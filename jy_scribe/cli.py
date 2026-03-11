"""CLI entry point for jy-scribe."""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from jy_scribe.audio import prepare_audio
from jy_scribe.transcribe import transcribe_audio, DEFAULT_MODEL
from jy_scribe.diarize import diarize_audio, assign_speakers_by_overlap
from jy_scribe.align import merge_consecutive
from jy_scribe.vtt import write_vtt


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="jy-scribe",
        description="Transcribe meeting recordings with speaker diarization → VTT",
    )
    parser.add_argument("input", help="Input audio/video file (.mp4, .m4a, .mp3, .wav)")
    parser.add_argument("-o", "--output", help="Output VTT path (default: <input>.vtt)")
    parser.add_argument("--num-speakers", type=int, help="Number of speakers (default: auto)")
    parser.add_argument("--language", help="Language code: zh, en (default: auto)")
    parser.add_argument("--prompt", help="Context prompt for better accuracy")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Whisper model (default: {DEFAULT_MODEL})")
    parser.add_argument("--no-diarize", action="store_true", help="Skip speaker diarization")
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> None:
    input_path = args.input
    if not os.path.isfile(input_path):
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or str(Path(input_path).with_suffix(".vtt"))

    # Step 1: Audio preparation
    print(f"[1/5] Preparing audio: {input_path}")
    t0 = time.time()
    wav_path = prepare_audio(input_path)
    print(f"      Done ({time.time() - t0:.1f}s)")

    try:
        # Step 2: Speech-to-text
        print(f"[2/5] Transcribing with {args.model}...")
        t0 = time.time()
        segments = transcribe_audio(
            wav_path,
            model=args.model,
            language=args.language,
            prompt=args.prompt,
        )
        print(f"      Done — {len(segments)} segments ({time.time() - t0:.1f}s)")

        if args.no_diarize:
            print("[3/5] Skipping diarization (--no-diarize)")
            print("[4/5] Skipping alignment")
            labeled_segments = segments
        else:
            # Step 3: Speaker diarization (pyannote — diarize-first)
            print("[3/5] Diarizing speakers (pyannote)...")
            t0 = time.time()
            turns = diarize_audio(wav_path, args.num_speakers)
            unique_speakers = len(set(t["speaker"] for t in turns))
            print(f"      Done — {unique_speakers} speakers, {len(turns)} turns ({time.time() - t0:.1f}s)")

            # Step 4: Align Whisper segments with pyannote turns and merge
            print("[4/5] Aligning segments with speakers...")
            labeled_segments = assign_speakers_by_overlap(segments, turns)
            labeled_segments = merge_consecutive(labeled_segments)
            print(f"      Done — {len(labeled_segments)} merged segments")

        # Step 5: Write VTT
        print(f"[5/5] Writing VTT: {output_path}")
        write_vtt(labeled_segments, output_path)
        print(f"\nComplete! Output: {output_path}")

    finally:
        # Clean up temp WAV
        if wav_path != input_path:
            os.unlink(wav_path)


def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
