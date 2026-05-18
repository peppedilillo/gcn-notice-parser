# GCN Parsers

`gcn-parser` is a Python 3.11+ package for parsing GCN Kafka messages or raw notice bytes into Pydantic models with named, typed fields.

## Installation

```shell
pip install gcn-parser
```

Live Kafka examples also need `gcn-kafka`:

```shell
pip install gcn-parser gcn-kafka
```

## Examples

### 1. Parse Live GCN Messages

```python
from gcn_kafka import Consumer

from gcn_parser import ParseError
from gcn_parser import SUPPORTED_TOPICS
from gcn_parser import parse


consumer = Consumer(
    # fill blanks with your GCN credentials
    client_id="...",
    client_secret="...",
    config={"auto.offset.reset": "earliest"},
)
consumer.subscribe(SUPPORTED_TOPICS)

while True:
    for message in consumer.consume(timeout=1):
        try:
            notice = parse(message)
        except ParseError as exc:
            print(f"Failed to parse {message.topic()}: {exc}")
            continue

        print(f"{message.topic()}: {type(notice).__name__}")
        print(notice)
```

### 2. Parse Selected Topics

Subscribe to selected topics when you know which notice family you want.
This example waits for one Fermi GBM final-position or ground-position notice and prints the burst position.

```python
from gcn_kafka import Consumer

from gcn_parser import ParseError
from gcn_parser import Topic
from gcn_parser import parse


consumer = Consumer(
    # fill blanks with your GCN credentials
    client_id="...",
    client_secret="...",
    config={"auto.offset.reset": "earliest"},
)
consumer.subscribe([Topic.FERMI_GBM_FIN_POS, Topic.FERMI_GBM_GND_POS])

while True:
    for message in consumer.consume(timeout=1):
        notice = parse(message)

        print(f"RA: {notice.ra} deg")
        print(f"Dec: {notice.dec} deg")
        print(f"Error radius: {notice.error_radius} deg")
```

### 3. Parse Notices on Disk

Use a mission-specific parser when you already know the notice type and have the raw notice stored on disk.

```python
from pathlib import Path

from gcn_parser.fermi import parse_fermi_gbm_fin_pos


notice = parse_fermi_gbm_fin_pos(Path("fermi_gbm_fin_pos.xml").read_bytes())

print(f"RA: {notice.ra} deg")
print(f"Dec: {notice.dec} deg")
print(f"Error radius: {notice.error_radius} deg")
```

Parsed notices are Pydantic models. Access fields directly, or inspect the full parsed payload with:

```python
notice.model_dump()
```

## Supported Topics

Currently supported GCN topics are:

```text
gcn.classic.voevent.FERMI_GBM_ALERT
gcn.classic.voevent.FERMI_GBM_FIN_POS
gcn.classic.voevent.FERMI_GBM_FLT_POS
gcn.classic.voevent.FERMI_GBM_GND_POS
gcn.classic.voevent.FERMI_LAT_OFFLINE
gcn.classic.voevent.FERMI_LAT_POS_DIAG
gcn.classic.voevent.FERMI_LAT_POS_INI
gcn.classic.voevent.FERMI_LAT_POS_UPD
gcn.notices.svom.voevent.grm
gcn.notices.svom.voevent.eclairs
gcn.notices.svom.voevent.mxt
gcn.notices.einstein_probe.wxt.alert
```

Swift is not operational at the moment, support will be added as soon as it gets back to operations (🤞) .
More will come eventually.

`SUPPORTED_TOPICS` is a list of all supported topics and can be passed directly to `Consumer.subscribe()`.

```python
from gcn_parser import SUPPORTED_TOPICS
from gcn_parser import Topic

print(Topic.FERMI_GBM_FIN_POS)
print(SUPPORTED_TOPICS)
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
