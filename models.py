"""Structured types for the Campus Customs vendor desk."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class DeskResult(BaseModel):
    """One vendor-document review for the buyer.

    Numbers come from the document. Decision follows handbook section 4:
    approved vendor, unit price at or under the SKU max, lead time 21 days or
    less, minimum order 600 or less. Any failed check is do_not_recommend.
    """

    vendor: str = Field(description="Vendor name as printed on the quote or email.")
    sku: str = Field(description="Campus Customs SKU, for example CC-HD-006.")
    unit_price: float | None = Field(
        default=None,
        description="Quoted unit price in USD. Null if the document does not state one.",
    )
    lead_time_days: int | None = Field(
        default=None,
        description="Lead time in days. Null if the document does not state one.",
    )
    min_order: int | None = Field(
        default=None,
        description="Minimum order in units. Null if the document does not state one.",
    )
    decision: Literal["recommend", "do_not_recommend"] = Field(
        description="recommend only when all four handbook checks pass."
    )
    reason: str = Field(
        description="One sentence that names the purchasing check that decided it."
    )
