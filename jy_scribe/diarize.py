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
    for seg in segments:
        audio_chunk = load_audio_segment(wav_path, seg["start"], seg["end"])
        if len(audio_chunk) < 1600:  # < 0.1s, too short
            embeddings.append(np.zeros(256, dtype=np.float32))
        else:
            embedding = encoder.embed_utterance(audio_chunk)
            embeddings.append(embedding)

    embeddings_array = np.array(embeddings)

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

    labels = clusterer.predict(embeddings_array)
    return labels.tolist()
