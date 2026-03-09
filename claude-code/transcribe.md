---
description: Transcribe a meeting recording with speaker diarization -- VTT
allowed-tools: Bash, Read
---

# /transcribe

Transcribe a meeting recording file using jy-scribe (local AI, no cloud).

## Usage

The user provides an audio/video file path. Run jy-scribe to transcribe it.

## Instructions

1. Confirm the input file exists
2. Activate the jy-scribe venv and run the CLI:

```bash
source ~/Documents/MyCode/claudeCodeRoot/jy-scribe/venv/bin/activate && \
jy-scribe "$ARGUMENTS"
```

3. Report the output path and any notable info (duration, speaker count)
4. If the user didn't specify options, use defaults (large-v3, auto language, diarization on)

## Common flags
- `--num-speakers N` — specify speaker count
- `--language zh` or `--language en` — force language
- `--prompt "會議主題"` — improve accuracy with context
- `--no-diarize` — skip speaker identification
- `-o path.vtt` — custom output path
