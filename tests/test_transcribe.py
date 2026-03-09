from unittest.mock import patch, MagicMock
from jy_scribe.transcribe import transcribe_audio, DEFAULT_MODEL, DEFAULT_PROMPT


def test_transcribe_calls_mlx_whisper():
    mock_result = {
        "text": "Hello",
        "language": "en",
        "segments": [
            {"id": 0, "start": 0.0, "end": 2.0, "text": "Hello"}
        ],
    }
    with patch("jy_scribe.transcribe.mlx_whisper") as mock_mlx:
        mock_mlx.transcribe.return_value = mock_result
        segments = transcribe_audio("test.wav")

        mock_mlx.transcribe.assert_called_once()
        call_kwargs = mock_mlx.transcribe.call_args
        assert call_kwargs[0][0] == "test.wav"
        assert len(segments) == 1
        assert segments[0]["text"] == "Hello"


def test_transcribe_passes_language():
    mock_result = {"text": "", "language": "zh", "segments": []}
    with patch("jy_scribe.transcribe.mlx_whisper") as mock_mlx:
        mock_mlx.transcribe.return_value = mock_result
        transcribe_audio("test.wav", language="zh")
        kwargs = mock_mlx.transcribe.call_args[1]
        assert kwargs["language"] == "zh"


def test_transcribe_passes_custom_prompt():
    mock_result = {"text": "", "language": "zh", "segments": []}
    with patch("jy_scribe.transcribe.mlx_whisper") as mock_mlx:
        mock_mlx.transcribe.return_value = mock_result
        transcribe_audio("test.wav", prompt="ZFS 技術會議")
        kwargs = mock_mlx.transcribe.call_args[1]
        assert "ZFS" in kwargs["initial_prompt"]


def test_transcribe_returns_simplified_segments():
    mock_result = {
        "text": "Hello",
        "language": "en",
        "segments": [
            {"id": 0, "seek": 0, "start": 0.0, "end": 2.0,
             "text": " Hello", "tokens": [1, 2, 3]}
        ],
    }
    with patch("jy_scribe.transcribe.mlx_whisper") as mock_mlx:
        mock_mlx.transcribe.return_value = mock_result
        segments = transcribe_audio("test.wav")
        seg = segments[0]
        assert set(seg.keys()) == {"start", "end", "text"}
        assert seg["text"] == "Hello"  # stripped leading space


def test_default_prompt_contains_traditional_chinese():
    assert "繁體中文" in DEFAULT_PROMPT
