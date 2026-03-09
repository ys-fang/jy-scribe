from unittest.mock import patch, MagicMock
from jy_scribe.cli import parse_args, run


def test_parse_args_minimal():
    args = parse_args(["meeting.mp4"])
    assert args.input == "meeting.mp4"
    assert args.output is None
    assert args.num_speakers is None
    assert args.language is None


def test_parse_args_all_options():
    args = parse_args([
        "meeting.mp4",
        "--output", "out.vtt",
        "--num-speakers", "3",
        "--language", "zh",
        "--prompt", "技術會議",
        "--model", "mlx-community/whisper-base",
    ])
    assert args.output == "out.vtt"
    assert args.num_speakers == 3
    assert args.language == "zh"
    assert args.prompt == "技術會議"
    assert args.model == "mlx-community/whisper-base"


def test_parse_args_no_diarize():
    args = parse_args(["meeting.mp4", "--no-diarize"])
    assert args.no_diarize is True


def test_run_calls_pipeline():
    """Verify run() calls each pipeline step in order."""
    with patch("jy_scribe.cli.prepare_audio") as mock_prep, \
         patch("jy_scribe.cli.transcribe_audio") as mock_stt, \
         patch("jy_scribe.cli.diarize_segments") as mock_diar, \
         patch("jy_scribe.cli.assign_speakers") as mock_assign, \
         patch("jy_scribe.cli.merge_consecutive") as mock_merge, \
         patch("jy_scribe.cli.write_vtt") as mock_write, \
         patch("os.path.isfile", return_value=True), \
         patch("os.unlink"):

        mock_prep.return_value = "/tmp/audio.wav"
        mock_stt.return_value = [{"start": 0, "end": 1, "text": "Hi"}]
        mock_diar.return_value = [0]
        mock_assign.return_value = [{"start": 0, "end": 1, "text": "Hi", "speaker": "Speaker 1"}]
        mock_merge.return_value = [{"start": 0, "end": 1, "text": "Hi", "speaker": "Speaker 1"}]

        args = parse_args(["meeting.mp4"])
        run(args)

        mock_prep.assert_called_once()
        mock_stt.assert_called_once()
        mock_diar.assert_called_once()
        mock_assign.assert_called_once()
        mock_merge.assert_called_once()
        mock_write.assert_called_once()
