# Campus Customs vendor desk (MGT 409 HW6)

PydanticAI agent on `gpt-6-luna`. Reads a vendor HTML quote, PDF, or `.eml`, checks it against `data/shop_handbook.md`, and returns recommend / do_not_recommend.

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# put OPENAI_API_KEY in .env (never commit .env)
```

## Run

```bash
python agent.py --doc data/practice_docs/p01_bluehen_quote.html
python agent.py --doc data/practice_docs/p08_chapelst_email.eml
```

`--unsafe` is the no-defense agent (used to measure attacks). `--no-cache` busts handbook prompt cache.

Write-up is `output/hw6_report.html`. Open that file in a browser; it does not need the network.
