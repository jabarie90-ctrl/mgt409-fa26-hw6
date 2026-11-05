# AI_prompts.md

Log of what was typed to the vibe coder. Runtime prompts the agent reads live in `prompts/`.

Created at the start of Homework 6. Each of Problems 2–10 has its own section and is filled only when that problem is actually worked.

---

## Problem 1: Vibe coder prompts

**Prompt I typed:** Let’s work through HW6 Problem 1 — start the vibe-coder log so we can do this homework one problem at a time.

**What was lacking after the first prompt:** (none yet)

**Evidence this was its own step:** `AI_prompts.md` exists with a section for each problem. Handbook sizing, the vendor-desk agent, and GitHub are later.

---

## Problem 2: Size up the handbook

**Prompt I typed:** Let’s work through problem 2.

**What was lacking after the first prompt:** (none yet)

**Evidence this was its own step:** unzipped `data.zip`, counted `shop_handbook.md` with tiktoken, wrote `output/handbook_estimate.md`. The vendor-desk agent is not in this step.

---

## Problem 3: Build the vendor desk agent

**Prompt I typed:** Ok lets go through the rest of this then we will do 5. Start with the vendor desk agent: PydanticAI, gpt-6-luna, the four files, it reads html/pdf/eml, trap tools only log, run p01 and p08.

**What was lacking after the first prompt:** (none)

**Evidence this was its own step:** `agent.py`, `tools.py`, `models.py`, `prompts/prompt.md`, `output/harness.md`. Ran `p01_bluehen_quote.html` and `p08_chapelst_email.eml`.

---

## Problem 4: With and without cached tokens

**Prompt I typed:** Run all 12 practice docs twice, once so the handbook is cached and once so cached tokens are actually zero. Put the dollars in cache_test.

**What was lacking after the first prompt:** First no-cache try still showed cached reads because the follow-up after read_document reused the same prefix. Needed a nonce on every model request, not once per document.

**Evidence this was its own step:** `output/cache_test.json` and `output/cache_test.md`. Without-cache cached-read tokens are 0 on every call.

---

## Problem 5: Attack your own agent

**Prompt I typed:** Run the undefended agent on the 12 practice docs, compare to the practice key, and write up what actually fooled it vs what a person sees.

**What was lacking after the first prompt:** (none)

**Evidence this was its own step:** `output/attack_results.json` and `output/attack_results.md`. Two PDFs fooled it; hidden HTML did not; trap_calls stayed empty.

---

## Problem 6: Defend your agent

**Prompt I typed:** Put three defense layers in, keep the trap tools on the system, keep --unsafe, rerun the 12, and do not blank the clean quotes.

**What was lacking after the first prompt:** (none)

**Evidence this was its own step:** sanitizer + Python handbook rules + prompt.md. `output/defense_results.json` 12/12 match. Safety section in `output/harness.md`.

---

## Problem 7: Red team

**Prompt I typed:** Make two new poisoned quotes that are not copies of the practice tricks, run them on unsafe and defended.

**What was lacking after the first prompt:** First pair (JSON-LD + markdown MIME) did not fool gpt-6-luna. Rebuilt as white-fill PDF text, which did.

**Evidence this was its own step:** `data/my_attacks/a01_yorkst_quote.pdf` and `a02_maplemills_quote.pdf`, `output/red_team.md`.

---

## Problem 8: Exam documents

**Prompt I typed:** Run the defended agent on the 10 exam docs and save exam_results.json with no hand edits.

**What was lacking after the first prompt:** (none)

**Evidence this was its own step:** `output/exam_results.json` written from the agent output only.

---

## Problem 9: Results page

**Prompt I typed:** One self-contained html report with the real cache numbers, attacks before/after, defense cost, exam, red team, and a monthly cost call for the store manager.

**What was lacking after the first prompt:** (none)

**Evidence this was its own step:** `output/hw6_report.html`.

---

## Problem 10: Push to GitHub and submit the URL

**Prompt I typed:** Public GitHub repo, full data folder, gitignore the .env, placeholders in .env.example.

**What was lacking after the first prompt:** (none)

**Evidence this was its own step:** https://github.com/jabarie90-ctrl/mgt409-fa26-hw6
