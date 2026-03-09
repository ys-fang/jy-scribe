import subprocess
from unittest.mock import patch, MagicMock
from jy_scribe.audio import prepare_audio, get_audio_duration


def test_prepare_audio_builds_correct_ffmpeg_command():
    """Verify ffmpeg is called with correct args for mono 16kHz WAV."""
    with patch("jy_scribe.audio.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = prepare_audio("meeting.mp4", "/tmp/output.wav")

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "ffmpeg" in cmd[0]
        assert "-ac" in cmd
        assert "1" in cmd
        assert "-ar" in cmd
        assert "16000" in cmd
        assert result == "/tmp/output.wav"


def test_prepare_audio_raises_on_failure():
    """Should raise RuntimeError if ffmpeg fails."""
    with patch("jy_scribe.audio.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="error")
        try:
            prepare_audio("bad.mp4", "/tmp/out.wav")
            assert False, "Should have raised"
        except RuntimeError as e:
            assert "ffmpeg" in str(e).lower()


def test_get_audio_duration():
    """Should parse duration from ffprobe output."""
    with patch("jy_scribe.audio.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0, stdout="125.340000\n"
        )
        duration = get_audio_duration("meeting.wav")
        assert abs(duration - 125.34) < 0.01
