"""Collect GCN VOEvent XML fixture files from the Kafka stream."""

import os
from pathlib import Path
import time

import click
from gcn_kafka import Consumer

TOPICS = {
    "fermi": [
        "gcn.classic.voevent.FERMI_GBM_ALERT",
        "gcn.classic.voevent.FERMI_GBM_FIN_POS",
        "gcn.classic.voevent.FERMI_GBM_FLT_POS",
        "gcn.classic.voevent.FERMI_GBM_GND_POS",
        "gcn.classic.voevent.FERMI_LAT_POS_INI",
        "gcn.classic.voevent.FERMI_LAT_POS_UPD",
        "gcn.classic.voevent.FERMI_LAT_POS_DIAG",
        "gcn.classic.voevent.FERMI_LAT_GND",
        "gcn.classic.voevent.FERMI_LAT_OFFLINE",
    ],
    "swift": [
        "gcn.classic.voevent.SWIFT_BAT_GRB_LC",
        "gcn.classic.voevent.SWIFT_BAT_GRB_LC_PROC",
        "gcn.classic.voevent.SWIFT_BAT_GRB_POS_ACK",
        "gcn.classic.voevent.SWIFT_BAT_GRB_POS_NACK",
        "gcn.classic.voevent.SWIFT_BAT_GRB_POS_TEST",
        "gcn.classic.voevent.SWIFT_BAT_KNOWN_SRC",
        "gcn.classic.voevent.SWIFT_BAT_MONITOR",
        "gcn.classic.voevent.SWIFT_BAT_QL_POS",
        "gcn.classic.voevent.SWIFT_BAT_SCALEDMAP",
        "gcn.classic.voevent.SWIFT_FOM_OBS",
        "gcn.classic.voevent.SWIFT_FOM_SAFE_POINT",
        "gcn.classic.voevent.SWIFT_FOM_SLEW_ABORT",
        "gcn.classic.voevent.SWIFT_SC_SLEW",
        "gcn.classic.voevent.SWIFT_TOO_FOM",
        "gcn.classic.voevent.SWIFT_TOO_SC_SLEW",
        "gcn.classic.voevent.SWIFT_UVOT_DBURST",
        "gcn.classic.voevent.SWIFT_UVOT_DBURST_PROC",
        "gcn.classic.voevent.SWIFT_UVOT_FCHART",
        "gcn.classic.voevent.SWIFT_UVOT_FCHART_PROC",
        "gcn.classic.voevent.SWIFT_UVOT_POS",
        "gcn.classic.voevent.SWIFT_UVOT_POS_NACK",
        "gcn.classic.voevent.SWIFT_XRT_CENTROID",
        "gcn.classic.voevent.SWIFT_XRT_IMAGE",
        "gcn.classic.voevent.SWIFT_XRT_IMAGE_PROC",
        "gcn.classic.voevent.SWIFT_XRT_LC",
        "gcn.classic.voevent.SWIFT_XRT_POSITION",
        "gcn.classic.voevent.SWIFT_XRT_SPECTRUM",
        "gcn.classic.voevent.SWIFT_XRT_SPECTRUM_PROC",
        "gcn.classic.voevent.SWIFT_XRT_SPER",
        "gcn.classic.voevent.SWIFT_XRT_SPER_PROC",
        "gcn.classic.voevent.SWIFT_XRT_THRESHPIX",
        "gcn.classic.voevent.SWIFT_XRT_THRESHPIX_PROC",
    ],
    "svom": [
        "gcn.notices.svom.voevent.grm",
        "gcn.notices.svom.voevent.eclairs",
        "gcn.notices.svom.voevent.mxt",
    ],
    "ep": [
        "gcn.notices.einstein_probe.wxt.alert",
    ],
    "lvc": [
        "gcn.classic.voevent.LVC_COUNTERPART",
        "gcn.classic.voevent.LVC_EARLY_WARNING",
        "gcn.classic.voevent.LVC_INITIAL",
        "gcn.classic.voevent.LVC_PRELIMINARY",
        "gcn.classic.voevent.LVC_RETRACTION",
        "gcn.classic.voevent.LVC_TEST",
        "gcn.classic.voevent.LVC_UPDATE",
    ],
}

SUFFIX = {
    "fermi": ".xml",
    "swift": ".xml",
    "svom": ".xml",
    "ep": ".json",
    "lvc": ".xml",
}

FIXTURES_ROOT = Path(__file__).resolve().parent


def channel_name(topic: str) -> str:
    return topic.rsplit(".", 1)[-1].lower()


def build_reverse_map(topics: dict) -> dict:
    return {topic: instrument for instrument, ts in topics.items() for topic in ts}


def count_existing(topics: dict) -> dict:
    counts = {}
    for instrument, topic_list in topics.items():
        for topic in topic_list:
            channel = channel_name(topic)
            d = FIXTURES_ROOT / instrument / channel
            counts[topic] = len(list(d.glob("*.xml"))) if d.exists() else 0
    return counts


def all_saturated(collected: dict, quota: int) -> bool:
    return all(n >= quota for n in collected.values())


def save_fixture(instrument: str, channel: str, offset: int, content: bytes) -> Path:
    dest = FIXTURES_ROOT / instrument / channel
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f"{channel}_{offset}{SUFFIX[instrument]}"
    path.write_bytes(content)
    return path


@click.command()
@click.option("--quota", default=10, show_default=True, help="Max fixtures per topic.")
@click.option("--timeout", default=30, show_default=True, help="Global timeout in seconds.")
def main(quota: int, timeout: int) -> None:
    collected = count_existing(TOPICS)

    if all_saturated(collected, quota):
        click.echo("All topics already at quota. Nothing to do.")
        return

    topic_to_instrument = build_reverse_map(TOPICS)
    all_topics = list(topic_to_instrument)

    consumer = Consumer(
        client_id=os.environ["GCN_CLIENT_ID"],
        client_secret=os.environ["GCN_CLIENT_SECRET"],
        config={
            "auto.offset.reset": "earliest",
        },
    )

    try:
        consumer.subscribe(all_topics)
        click.echo(f"Subscribed to {len(all_topics)} topics. Collecting up to {quota} fixtures each.")

        deadline = time.monotonic() + timeout
        while not all_saturated(collected, quota) and time.monotonic() < deadline:
            for message in consumer.consume(timeout=1):
                if message.error():
                    click.echo(f"Error: {message.error()}", err=True)
                    continue

                topic = message.topic()
                if collected.get(topic, 0) >= quota:
                    continue

                instrument = topic_to_instrument[topic]
                channel = channel_name(topic)
                path = save_fixture(instrument, channel, message.offset(), message.value())
                collected[topic] = collected.get(topic, 0) + 1
                click.echo(f"Saved {path.relative_to(FIXTURES_ROOT.parent.parent)}")

                if all_saturated(collected, quota):
                    break
    finally:
        consumer.close()

    saturated = sum(1 for n in collected.values() if n >= quota)
    click.echo(f"Done. {saturated}/{len(collected)} topics at quota ({quota}).")


if __name__ == "__main__":
    main()
