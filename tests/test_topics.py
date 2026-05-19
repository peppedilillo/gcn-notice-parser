from gcn_parser import SUPPORTED_TOPICS
from gcn_parser import supported_topics
from gcn_parser.topics import Topic


def test_topic_is_string_like():
    topic = Topic.FERMI_GBM_FIN_POS

    assert isinstance(topic, str)
    assert topic == topic.value
    assert str(topic) == topic.value


def test_supported_topics_returns_all_topics():
    assert supported_topics() == list(Topic)


def test_supported_topics_returns_new_list():
    topics = supported_topics()
    topics.pop()

    assert supported_topics() == list(Topic)


def test_supported_topics_constant_matches_topics():
    assert SUPPORTED_TOPICS == list(Topic)
