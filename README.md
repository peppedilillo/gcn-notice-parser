# GCN Parsers

Typed parsers for selected GCN / VOEvent notice families.

The package is organized by mission:
- `gcnparser.fermi`
- `gcnparser.svom`

Current coverage:
- `Fermi / GBM`: alert, flt pos, gnd pos, fin pos
- `Fermi / LAT`: initial pos, updated pos, final/diag pos, offline pos
- `SVOM / ECLAIRs`: unified non-retraction notices
- `SVOM / GRM`: trigger notices
- `SVOM / MXT`: unified notices
- `SVOM`: generic packet-219 retractions

Parsers accept raw XML `bytes` and return typed Pydantic models. Parsed models preserve the raw VOEvent `ivorn` and expose mission-specific fields extracted from the notice body.

## Usage

```python
from pathlib import Path

from gcnparser.fermi import parse_fermi_gbm_alert
from gcnparser.svom import parse_svom_eclairs

fermi_notice = parse_fermi_gbm_alert(Path("notice.xml").read_bytes())
print(fermi_notice.ivorn)
print(fermi_notice.trig_id)

svom_notice = parse_svom_eclairs(Path("svom_notice.xml").read_bytes())
print(svom_notice.ivorn)
print(svom_notice.packet_type)
```

## Package Layout

- `gcnparser.parse_xml`: shared XML parsing helpers and parse-error boundary
- `gcnparser.fermi`: Fermi notice models and parser entrypoints
- `gcnparser.svom`: SVOM notice models and parser entrypoints

The stable public entrypoints currently live under the mission subpackages rather than the top-level `gcnparser` namespace.

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
