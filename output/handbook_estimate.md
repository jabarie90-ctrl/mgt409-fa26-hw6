# Handbook token estimate

File: `data/shop_handbook.md`  
Model prices: `data/prices.json` → `gpt-6-luna`

## Token count

**10,058 tokens.**

How I got it: I did not guess from characters. I loaded the whole markdown file and counted with `tiktoken` encoding `o200k_base` (the encoding current OpenAI chat models use; `gpt-6-luna` is not in tiktoken’s named-model list). `cl100k_base` came out 10,184; I am using 10,058.

Sanity check on the file itself: 28,903 characters, 6,127 words, 339 lines. A lazy “chars ÷ 4” guess would have been ~7,226, which is too low. The assignment said the handbook is about 10,000 tokens; the tokenizer agrees.

The agent will send this handbook on **every** call, so this is the repeating input bill before the vendor document even shows up.

## Prices used (`gpt-6-luna`, per 1M tokens)

| Kind | $/1M |
|---|---|
| Uncached input | 0.10 |
| Cached input | 0.01 |
| Cache write | 0.125 |
| Output | 0.50 |

This estimate is **handbook input only**. No output tokens, no quote text.

Let \(N = 10058\).

## Without cache (pay full input every time)

One call:

\[
10058 / 1{,}000{,}000 \times 0.10 = \$0.0010058
\]

1,000 calls:

\[
1000 \times 0.0010058 = \$1.0058
\]

## With cached tokens

Once the handbook is already in cache, each later call pays the cached-input rate:

One warm call:

\[
10058 / 1{,}000{,}000 \times 0.01 = \$0.00010058
\]

1,000 warm calls (handbook already cached):

\[
1000 \times 0.00010058 = \$0.10058
\]

That is about **90% cheaper** than the no-cache bill (\(1.0058 - 0.10058 = 0.90522\), save \(0.90522 / 1.0058 \approx 90\%\)).

### First call is a cache write, not a cache read

`prices.json` also lists `cache_write_per_1m` at **0.125**, which is *higher* than plain input (0.10). So the first time you fill the cache:

\[
10058 / 1{,}000{,}000 \times 0.125 = \$0.00125725
\]

A realistic 1,000-call day (one write, then 999 cached reads):

\[
0.00125725 + 999 \times 0.00010058 = \$0.10174
\]

Still about **\$0.90** cheaper than 1,000 uncached calls.

I will check these numbers against real API token counts in Problem 4.
