# Developer Guide

## Setup

Clone the repository and install the development dependencies.

```bash
git clone https://github.com/peppedilillo/gcn-notice-parser.git
cd gcn-notice-parser
uv sync --group dev
```

## Pre-commit Hooks

Install the hooks before committing.

```bash
uv run pre-commit install
```

The hooks run `black`, `isort`, and basic file checks.

## Running Tests

Run the test suite from the project directory.

```bash
uv run pytest -q
```

## Collecting Fixtures

Fixture collection reads messages from GCN Kafka and writes notice payloads
under `tests/fixtures`.

```bash
cp .secrets.sample .secrets
vim .secrets
source .secrets
uv run tests/fixtures/collect_fixtures.py --help
```

The `.secrets` file must define the environment variables `GCN_CLIENT_ID` and `GCN_CLIENT_SECRET`.

## Documentation

Serve the documentation locally.

```bash
uv run mkdocs serve
```

Deploy the documentation to GitHub Pages.

```bash
uv run mkdocs gh-deploy
```
