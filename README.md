# GCN Parsers


## Usage

```python
from pathlib import Path

from gcn_parser.fermi import parse_fermi_gbm_alert
from gcn_parser.svom import parse_svom_eclairs

fermi_notice = parse_fermi_gbm_alert(Path("notice.xml").read_bytes())
print(fermi_notice.ivorn)
print(fermi_notice.trig_id)

svom_notice = parse_svom_eclairs(Path("svom_notice.xml").read_bytes())
print(svom_notice.ivorn)
print(svom_notice.packet_type)
```

## Development

Run tests:

```shell
uv run pytest -q
```

Collect fixtures for testing:

```shell
cp .secrets.sample .secrets
vim .secrets  # fill GCN credentials
source .secrets
uv run tests/fixtures/collect_fixtures.py --help
```
