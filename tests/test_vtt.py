from jy_scribe.vtt import format_timestamp, format_vtt


def test_format_timestamp_zero():
    assert format_timestamp(0.0) == "00:00:00.000"


def test_format_timestamp_seconds():
    assert format_timestamp(5.6) == "00:00:05.600"


def test_format_timestamp_minutes():
    assert format_timestamp(125.3) == "00:02:05.300"


def test_format_timestamp_hours():
    assert format_timestamp(3725.1) == "01:02:05.100"


def test_format_vtt_single_segment():
    segments = [
        {"start": 1.5, "end": 4.2, "text": "Hello world", "speaker": "Speaker 1"}
    ]
    result = format_vtt(segments)
    expected = (
        "WEBVTT\n"
        "\n"
        "1\n"
        "00:00:01.500 --> 00:00:04.200\n"
        "<v Speaker 1>Hello world\n"
    )
    assert result == expected


def test_format_vtt_multiple_segments():
    segments = [
        {"start": 1.5, "end": 4.2, "text": "我們來討論", "speaker": "Speaker 1"},
        {"start": 4.8, "end": 7.1, "text": "好的", "speaker": "Speaker 2"},
    ]
    result = format_vtt(segments)
    assert "WEBVTT" in result
    assert "<v Speaker 1>我們來討論" in result
    assert "<v Speaker 2>好的" in result
    assert result.count("-->") == 2


def test_format_vtt_no_speaker():
    segments = [
        {"start": 0.0, "end": 2.0, "text": "No speaker info"}
    ]
    result = format_vtt(segments)
    assert "<v" not in result
    assert "No speaker info" in result
