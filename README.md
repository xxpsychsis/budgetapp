# Budget Helper

This project provides a simple command line helper for [YNAB](https://www.youneedabudget.com/) budgets. It can fetch your budget categories, suggest moves to cover overspending and, if requested, apply those changes using the YNAB API.

## Requirements

- Python 3.8+
- `requests` (see `requirements.txt`)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Set the environment variable `YNAB_TOKEN` to your personal access token. Then run:

```bash
python budget_cli.py <budget_id>
```

Add `--apply` to automatically make the suggested adjustments. You can also specify a month with `--month YYYY-MM-01`.

## Development

Tests can be run with:

```bash
pytest
```

