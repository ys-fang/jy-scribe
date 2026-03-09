"""Align STT segments with speaker diarization labels."""


def assign_speakers(
    stt_segments: list[dict],
    speaker_labels: list[int],
) -> list[dict]:
    """Assign speaker labels to STT segments.

    Args:
        stt_segments: List of {"start", "end", "text"} from whisper.
        speaker_labels: List of int cluster IDs from spectralcluster.

    Returns:
        New list of segments with "speaker" field added.
    """
    result = []
    for seg, label in zip(stt_segments, speaker_labels):
        new_seg = dict(seg)
        new_seg["speaker"] = f"Speaker {label + 1}"
        result.append(new_seg)
    return result


def merge_consecutive(segments: list[dict]) -> list[dict]:
    """Merge consecutive segments from the same speaker."""
    if not segments:
        return []

    merged = [dict(segments[0])]

    for seg in segments[1:]:
        prev = merged[-1]
        if seg.get("speaker") == prev.get("speaker"):
            prev["end"] = seg["end"]
            prev["text"] = prev["text"] + " " + seg["text"]
        else:
            merged.append(dict(seg))

    return merged
