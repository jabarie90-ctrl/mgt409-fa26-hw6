"""Parse the shop handbook and apply the four purchasing checks."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HANDBOOK_PATH = ROOT / "data" / "shop_handbook.md"
MAX_LEAD_DAYS = 21
MAX_MIN_ORDER = 600


@dataclass(frozen=True)
class Handbook:
    approved: tuple[str, ...]
    removed: tuple[str, ...]
    max_unit_cost: dict[str, float]
    text: str


def _section(text: str, number: int) -> str:
    parts = re.split(r"\n## ", text)
    prefix = f"{number}."
    for part in parts:
        chunk = part if part.startswith("#") else f"## {part}"
        heading = chunk.split("\n", 1)[0]
        if re.search(rf"##\s+{number}\.", heading):
            return chunk
    raise KeyError(f"handbook section {number} not found")


def _table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0].lower() in {"code", "vendor", "sku", "po"}:
            continue
        rows.append(cells)
    return rows


@lru_cache(maxsize=1)
def load_handbook() -> Handbook:
    text = HANDBOOK_PATH.read_text(encoding="utf-8")
    approved = tuple(row[1] for row in _table_rows(_section(text, 5)) if len(row) >= 2)
    removed = tuple(row[0] for row in _table_rows(_section(text, 6)) if row)
    costs: dict[str, float] = {}
    for row in _table_rows(_section(text, 9)):
        if len(row) < 5:
            continue
        sku = row[0]
        if not re.fullmatch(r"CC-[A-Z]{2}-\d{3}", sku):
            continue
        costs[sku] = float(row[4].replace("$", "").replace(",", ""))
    return Handbook(approved=approved, removed=removed, max_unit_cost=costs, text=text)


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip().lower()


def match_vendor(name: str) -> tuple[str | None, str]:
    """Return (canonical name, status) where status is approved, removed, or unknown."""
    book = load_handbook()
    needle = _norm(name)
    if not needle:
        return None, "unknown"
    for vendor in book.removed:
        if _norm(vendor) in needle or needle in _norm(vendor):
            return vendor, "removed"
    for vendor in book.approved:
        if _norm(vendor) in needle or needle in _norm(vendor):
            return vendor, "approved"
    return name.strip() or None, "unknown"


def find_vendor_in_text(text: str) -> str | None:
    book = load_handbook()
    hay = text.lower()
    hits: list[tuple[int, str]] = []
    for name in (*book.removed, *book.approved):
        idx = hay.find(name.lower())
        if idx >= 0:
            hits.append((idx, name))
    if not hits:
        return None
    return min(hits, key=lambda item: item[0])[1]


def apply_rules(
    vendor: str,
    sku: str,
    unit_price: float | None,
    lead_time_days: int | None,
    min_order: int | None,
) -> tuple[str, str]:
    """Return (decision, reason) from handbook section 4. Code, not the model."""
    book = load_handbook()
    canonical, status = match_vendor(vendor)
    label = canonical or vendor or "Unknown vendor"
    if status != "approved":
        if status == "removed":
            return (
                "do_not_recommend",
                f"{label} is on the removed or pending list in handbook section 6.",
            )
        return (
            "do_not_recommend",
            f"{label} is not on the approved vendor list in handbook section 5.",
        )
    sku = (sku or "").strip().upper()
    if sku not in book.max_unit_cost:
        return "do_not_recommend", f"SKU {sku or '(missing)'} is not in the catalogue."
    cap = book.max_unit_cost[sku]
    if unit_price is None:
        return "do_not_recommend", "Unit price is unknown, so the price check cannot pass."
    if unit_price > cap:
        return (
            "do_not_recommend",
            f"Unit price ${unit_price:.2f} is above the max unit cost ${cap:.2f} for {sku}.",
        )
    if lead_time_days is None:
        return "do_not_recommend", "Lead time is unknown, so the lead-time check cannot pass."
    if lead_time_days > MAX_LEAD_DAYS:
        return (
            "do_not_recommend",
            f"Lead time {lead_time_days} days is over the {MAX_LEAD_DAYS}-day limit.",
        )
    if min_order is None:
        return "do_not_recommend", "Minimum order is unknown, so the min-order check cannot pass."
    if min_order > MAX_MIN_ORDER:
        return (
            "do_not_recommend",
            f"Minimum order {min_order} units is over the {MAX_MIN_ORDER}-unit limit.",
        )
    return (
        "recommend",
        (
            f"{label} is approved, unit price ${unit_price:.2f} is at or under ${cap:.2f}, "
            f"lead time {lead_time_days} days, minimum order {min_order}."
        ),
    )
