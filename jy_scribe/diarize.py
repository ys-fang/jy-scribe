"""Speaker diarization using pyannote.audio."""
from __future__ import annotations

from typing import List, Optional

import torch
from pyannote.audio import Pipeline


def _get_device() -> torch.device:
    """Pick the best available device: MPS (Apple Silicon) > CUDA > CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def diarize_audio(
    wav_path: str,
    num_speakers: Optional[int] = None,
) -> list[dict]:
    """Run speaker diarization on the full audio file.

    Returns a list of speaker turns: [{"start": float, "end": float, "speaker": str}, ...]
    """
    device = _get_device()
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
    pipeline.to(device)

    result = pipeline(
        wav_path,
        num_speakers=num_speakers,
    )

    # pyannote 4.x returns DiarizeOutput; get the Annotation object
    annotation = getattr(result, "speaker_diarization", result)

    turns = []
    for turn, _, speaker in annotation.itertracks(yield_label=True):
        turns.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker,
        })
    return turns


def assign_speakers_by_overlap(
    segments: List[dict],
    turns: list[dict],
) -> List[dict]:
    """Assign speaker labels to Whisper segments based on pyannote diarization.

    For each Whisper segment, find the pyannote turn with the most overlap
    and assign that speaker.
    """
    # Build a mapping from pyannote speaker IDs to sequential labels
    unique_speakers = list(dict.fromkeys(t["speaker"] for t in turns))
    speaker_map = {s: f"Speaker {i + 1}" for i, s in enumerate(unique_speakers)}

    result = []
    for seg in segments:
        seg_start = seg["start"]
        seg_end = seg["end"]

        # Find overlapping turns and pick the one with most overlap
        best_speaker = None
        best_overlap = 0.0

        for turn in turns:
            overlap_start = max(seg_start, turn["start"])
            overlap_end = min(seg_end, turn["end"])
            overlap = max(0.0, overlap_end - overlap_start)

            if overlap > best_overlap:
                best_overlap = overlap
                best_speaker = turn["speaker"]

        new_seg = dict(seg)
        if best_speaker is not None:
            new_seg["speaker"] = speaker_map[best_speaker]
        result.append(new_seg)

    return result
