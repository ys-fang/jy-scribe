from jy_scribe.align import assign_speakers, merge_consecutive


def test_assign_speakers_basic():
    stt_segments = [
        {"start": 0.0, "end": 3.0, "text": "Hello"},
        {"start": 3.5, "end": 6.0, "text": "Hi there"},
        {"start": 6.5, "end": 9.0, "text": "How are you"},
    ]
    speaker_labels = [0, 1, 0]

    result = assign_speakers(stt_segments, speaker_labels)

    assert result[0]["speaker"] == "Speaker 1"
    assert result[1]["speaker"] == "Speaker 2"
    assert result[2]["speaker"] == "Speaker 1"
    assert result[0]["text"] == "Hello"
    assert result[0]["start"] == 0.0


def test_assign_speakers_preserves_original():
    stt_segments = [{"start": 0.0, "end": 1.0, "text": "Test"}]
    speaker_labels = [0]
    assign_speakers(stt_segments, speaker_labels)
    assert "speaker" not in stt_segments[0]


def test_merge_consecutive_same_speaker():
    segments = [
        {"start": 0.0, "end": 3.0, "text": "Hello", "speaker": "Speaker 1"},
        {"start": 3.1, "end": 5.0, "text": "world", "speaker": "Speaker 1"},
        {"start": 5.5, "end": 8.0, "text": "Hi", "speaker": "Speaker 2"},
    ]
    result = merge_consecutive(segments)
    assert len(result) == 2
    assert result[0]["text"] == "Hello world"
    assert result[0]["start"] == 0.0
    assert result[0]["end"] == 5.0
    assert result[1]["speaker"] == "Speaker 2"


def test_merge_consecutive_alternating():
    segments = [
        {"start": 0.0, "end": 2.0, "text": "A", "speaker": "Speaker 1"},
        {"start": 2.5, "end": 4.0, "text": "B", "speaker": "Speaker 2"},
        {"start": 4.5, "end": 6.0, "text": "C", "speaker": "Speaker 1"},
    ]
    result = merge_consecutive(segments)
    assert len(result) == 3


def test_merge_consecutive_empty():
    assert merge_consecutive([]) == []
