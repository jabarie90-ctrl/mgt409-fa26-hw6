# Cache test

Ran all 12 practice documents two ways on `gpt-6-luna`. Every call is in `cache_test.json`.
Each document is two model requests (read the file, then return the structured answer), so the handbook is sent twice.

## Totals

| Setup | Docs | Input tokens | Cached (read) tokens | Cache write tokens | Output tokens | Total $ | $ per doc |
|---|---:|---:|---:|---:|---:|---:|---:|
| With cache | 12 | 260053 | 242433 | 14596 | 2369 | 0.005736 | 0.000478 |
| Without cache | 12 | 260665 | 0 | 257641 | 2665 | 0.033840 | 0.002820 |

Saved 0.028104 dollars on this 12-doc set, **83.1%**.

Without-cache cached-read tokens were **zero on every call**. That was the check. I busted the prefix with a fresh nonce on every model request, including the follow-up after `read_document`. If I only changed the nonce once per document, the second request of the same run reused the handbook and showed cached tokens.

## vs Problem 2 estimate

Problem 2 counted the handbook at **10,058 tokens** and priced one handbook-only call at $0.001006 with no cache and $0.000101 when warm.

Real calls are larger: two requests plus the quote, the prompt, and tool schemas. Warm with-cache documents landed around $0.000419 to $0.000440, not $0.000101. The shape still matches: after the first document, cached reads sit around 21,080 tokens (handbook twice).

## 1,000 documents a day for 30 days

Using this run's average cost per document:

- With cache: 1,000 × 30 × $0.000478 = **$14.34**
- Without cache: 1,000 × 30 × $0.002820 = **$84.60**

About **$70.26** left on the table each month if the shop does not cache the handbook.

## What surprised me

Without cache **costs more than the plain input price**. OpenAI still writes the prefix into cache on every unique nonce (`cache_write_per_1m` = $0.125 vs input $0.10). The without-cache setup pays that write rate on ~21k tokens per document and never reads it back. Cached reads were zero, as required, but the bill is higher than "just pay $0.10 / 1M input." Problem 2 already flagged that the first write is more expensive than uncached input; here every no-cache document is a first write, twice.
