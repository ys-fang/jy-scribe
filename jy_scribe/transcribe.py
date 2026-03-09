"""Speech-to-text using mlx-whisper."""
from __future__ import annotations

try:
    import mlx_whisper
except ImportError:
    mlx_whisper = None  # Will be mocked in tests

DEFAULT_MODEL = "mlx-community/whisper-large-v3-mlx"
DEFAULT_PROMPT = "以下是繁體中文的會議語音轉錄。"


def transcribe_audio(
    wav_path: str,
    model: str = DEFAULT_MODEL,
    language: str | None = None,
    prompt: str | None = None,
) -> list[dict]:
    """Transcribe audio file using mlx-whisper."""
    if mlx_whisper is None:
        raise RuntimeError("mlx-whisper is not installed. Run: pip install mlx-whisper")

    initial_prompt = prompt if prompt is not None else DEFAULT_PROMPT

    result = mlx_whisper.transcribe(
        wav_path,
        path_or_hf_repo=model,
        language=language,
        initial_prompt=initial_prompt,
        word_timestamps=False,
        fp16=True,
    )

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })

    return segments
