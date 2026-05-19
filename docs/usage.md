# Usage Guide

## Live Kafka Messages

Use `parse` when you consume messages from GCN Kafka. The message object must
provide `topic()` and `value()` methods.

```python
from gcn_parser import ParseError
from gcn_parser import parse

try:
    # message is a kafka `Message` instance, or exposes `.value()` and `.topic()` methods
    notice = parse(message)
except ParseError as exc:
    print(f"Failed to parse {message.topic()}: {exc}")
```

## Raw Notice Bytes

Use a mission-specific parser when you already know the notice type and have
the notice payload as bytes. You can use the method `read_bytes()` of `pathlib.Path`
for reading a file as bytes.

```python
from pathlib import Path
from gcn_parser.fermi import parse_fermi_gbm_fin_pos

# parse a notice on file by first converting it to bytes
notice = parse_fermi_gbm_fin_pos(Path("fermi_gbm_fin_pos.xml").read_bytes())
```

```python
from pathlib import Path
from gcn_parser.fermi import parse_fermi_gbm_fin_pos

# parse a Kafka message payload 
notice = parse_fermi_gbm_fin_pos(message.value())
```

## Topics

Use `supported_topics()` to subscribe to every topic currently supported by
`gcn-parser`, or to check a list of supported topics.

```python
from gcn_parser import supported_topics

consumer.subscribe(supported_topics())
```

Use `Topic` when you want to subscribe to a specific set of topics.

```python
from gcn_parser import Topic

consumer.subscribe([Topic.FERMI_GBM_FIN_POS, Topic.FERMI_GBM_GND_POS])
```

## Errors

Catch `ParseError` around live consumers and continue processing later
messages. More specific exceptions are available when you need them.

```python
from gcn_parser import FieldParseError
from gcn_parser import ParseError
from gcn_parser import UnsupportedTopicError
from gcn_parser import parse

try:
    notice = parse(message)
except UnsupportedTopicError:
    print(f"Unsupported topic: {message.topic()}")
except FieldParseError as exc:
    print(f"Missing or invalid field: {exc}")
except ParseError as exc:
    print(f"Malformed notice payload: {exc}")
```

## Parsed Notices

Parsed notices are Pydantic models. Access fields directly or serialize the
model when you need a plain dict or JSON representation.

```python
print(notice.ra)
print(notice.dec)

payload = notice.model_dump()
json_payload = notice.model_dump_json()
```
