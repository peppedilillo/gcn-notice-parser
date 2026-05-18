from gcn_parser.topics import Topic


def test_topic_is_string_like():
    topic = Topic.FERMI_GBM_FIN_POS

    assert isinstance(topic, str)
    assert topic == topic.value
    assert str(topic) == topic.value
