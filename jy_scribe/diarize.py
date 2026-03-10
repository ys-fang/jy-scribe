"""Speaker diarization using resemblyzer + spectralcluster."""
from __future__ import annotations

from typing import List, Optional

import numpy as np

try:
    from resemblyzer import VoiceEncoder, preprocess_wav
except ImportError:
    VoiceEncoder = None
    preprocess_wav = None

try:
    from spectralcluster import SpectralClusterer
except ImportError:
    SpectralClusterer = None

try:
    import soundfile as sf
except ImportError:
    sf = None


def load_audio_segment(
    wav_path: str, start: float, end: float, sr: int = 16000
) -> np.ndarray:
    """Load a segment of audio from a WAV file."""
    start_frame = int(start * sr)
    num_frames = int((end - start) * sr)
    data, _ = sf.read(wav_path, start=start_frame, frames=num_frames, dtype="float32")
    return data


def diarize_segments(
    wav_path: str,
    segments: List[dict],
    num_speakers: Optional[int] = None,
) -> List[int]:
    """Assign speaker labels to segments via voice embedding clustering."""
    encoder = VoiceEncoder()

    embeddings = []
    valid_indices = []
    for i, seg in enumerate(segments):
        audio_chunk = load_audio_segment(wav_path, seg["start"], seg["end"])
        if len(audio_chunk) < 1600:  # < 0.1s, too short
            embeddings.append(None)
        else:
            embedding = encoder.embed_utterance(audio_chunk)
            embeddings.append(embedding)
            valid_indices.append(i)

    valid_embeddings = np.array([embeddings[i] for i in valid_indices])

    if num_speakers is not None:
        clusterer = SpectralClusterer(
            min_clusters=num_speakers,
            max_clusters=num_speakers,
        )
    else:
        clusterer = SpectralClusterer(
            min_clusters=2,
            max_clusters=10,
            autotune=True,
        )

    valid_labels = clusterer.predict(valid_embeddings)

    # Backfill: assign skipped segments the same label as the nearest valid one
    labels = [0] * len(segments)
    for j, idx in enumerate(valid_indices):
        labels[idx] = int(valid_labels[j])
    for i in range(len(segments)):
        if i not in valid_indices:
            # Find nearest valid segment
            nearest = min(valid_indices, key=lambda vi: abs(vi - i))
            labels[i] = labels[nearest]
    return labels
