# GCN Parsers

### Development

Collecting fixtures for testing:

```shell
cp .secrets.sample .secrets
vim .secrets # fill GCN credentials
source .secrets
uv run tests/fixtures/collect_fixtures.py --help
```

