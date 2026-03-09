"""VTT output formatter."""


def format_timestamp(seconds: float) -> str:
    """Convert seconds to VTT timestamp format HH:MM:SS.mmm."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds % 1) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def format_vtt(segments: list) -> str:
    """Format segments into a VTT string.

    Each segment dict has: start, end, text, and optionally speaker.
    """
    lines = ["WEBVTT", ""]

    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        lines.append(f"{start} --> {end}")

        text = seg["text"]
        speaker = seg.get("speaker")
        if speaker:
            lines.append(f"<v {speaker}>{text}")
        else:
            lines.append(text)
        lines.append("")

    return "\n".join(lines)


def write_vtt(segments: list, output_path: str) -> None:
    """Write segments to a VTT file."""
    content = format_vtt(segments)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
