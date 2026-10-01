#!/usr/bin/env bash
# One-time setup for the 8-Bit Backstory engine (Linux / Claude workspace).
# Installs ffmpeg + espeak-ng, the Python packages, and downloads the Kokoro voice model.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
SUDO=""; [ "$(id -u)" != "0" ] && command -v sudo >/dev/null && SUDO="sudo -n"
if ! command -v ffmpeg >/dev/null || ! command -v espeak-ng >/dev/null; then
  $SUDO apt-get update -qq && $SUDO apt-get install -y -qq ffmpeg espeak-ng >/dev/null
fi
pip install -q --break-system-packages numpy pillow onnxruntime kokoro-onnx soundfile num2words 2>/dev/null \
  || pip install -q numpy pillow onnxruntime kokoro-onnx soundfile num2words
mkdir -p "$D/models"
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s "$D/models/kokoro.onnx" ] || curl -sSL -o "$D/models/kokoro.onnx" "$REL/kokoro-v1.0.int8.onnx"
[ -s "$D/models/voices.bin" ]  || curl -sSL -o "$D/models/voices.bin"  "$REL/voices-v1.0.bin"
python3 -c "import kokoro_onnx, num2words, PIL, numpy; print('engine ready')"
