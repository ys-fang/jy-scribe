# jy-scribe

Local meeting transcription with speaker diarization -- VTT. 100% on-device, no cloud.

## Features

- Local speech-to-text via mlx-whisper (Apple MLX framework)
- Speaker diarization with resemblyzer + spectralcluster
- VTT output with `<v Speaker N>` labels
- Traditional Chinese and English support
- Optimized for macOS Apple Silicon (M1/M2/M3/M4)

## Requirements

- macOS with Apple Silicon
- Python 3.12+
- ffmpeg (`brew install ffmpeg`)

## Quick Start

```bash
git clone https://github.com/ys-fang/jy-scribe.git
cd jy-scribe
./install.sh
```

The installer creates a Python virtual environment, installs all dependencies, and registers the `jy-scribe` CLI command.

## Usage

```bash
# Basic — outputs meeting.vtt alongside the input file
jy-scribe meeting.mp4

# With options
jy-scribe meeting.mp4 --num-speakers 3 --language zh --prompt "Q2 roadmap 技術會議"

# Skip diarization
jy-scribe recording.m4a --no-diarize
```

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `-o`, `--output` | Output VTT file path | `<input>.vtt` |
| `--num-speakers` | Number of speakers | auto-detect |
| `--language` | Language code (`zh`, `en`) | auto-detect |
| `--prompt` | Context prompt for accuracy | Traditional Chinese default |
| `--model` | Whisper model identifier | `mlx-community/whisper-large-v3-mlx` |
| `--no-diarize` | Skip speaker diarization | off |

## VTT Output Example

```
WEBVTT

1
00:00:01.200 --> 00:00:04.800
<v Speaker 1>大家好，我們開始今天的會議。

2
00:00:05.100 --> 00:00:08.600
<v Speaker 2>好的，先來看上週的進度。

3
00:00:09.000 --> 00:00:12.300
<v Speaker 1>第一個議題是 Q2 的技術規劃。
```

## Claude Code Integration

jy-scribe includes a Claude Code skill file for the `/transcribe` command.

**Setup:**

```bash
cp claude-code/transcribe.md ~/.claude/commands/
```

**Usage in Claude Code:**

```
/transcribe meeting.mp4
/transcribe recording.m4a --num-speakers 3 --language zh
```

Claude Code will activate the jy-scribe environment, run the transcription, and report the results.

## How It Works

```
Input (.mp4/.m4a)
  |
  v
[1] ffmpeg --- extract/convert to 16kHz mono WAV
  |
  v
[2] mlx-whisper --- speech-to-text, returns timed segments
  |
  v
[3] resemblyzer + spectralcluster --- speaker embeddings + clustering
  |
  v
[4] Align --- assign speaker labels, merge consecutive same-speaker segments
  |
  v
[5] Write VTT --- output with <v Speaker N> tags
```

## AI Models Used

| Component | Model | Purpose |
|-----------|-------|---------|
| STT | [Whisper large-v3](https://huggingface.co/mlx-community/whisper-large-v3-mlx) (MLX) | Speech-to-text |
| Speaker embeddings | [resemblyzer](https://github.com/resemble-ai/Resemblyzer) | Voice fingerprinting |
| Speaker clustering | [spectralcluster](https://github.com/wq2012/SpectralCluster) | Group embeddings into speakers |

## License

Apache License 2.0. See [LICENSE](LICENSE).
