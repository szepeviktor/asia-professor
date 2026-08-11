#!/usr/bin/env bash
set -euo pipefail

mkdir -p assets

prepare_image() {
  local slug="$1"
  ffmpeg -y -loglevel error \
    -i "downloads/${slug}.jpg" \
    -vf "scale=900:720:force_original_aspect_ratio=decrease,pad=900:720:(ow-iw)/2:(oh-ih)/2:color=151a20" \
    "assets/${slug}.png"
}

prepare_video() {
  local source="$1"
  local slug="$2"
  ffmpeg -y -loglevel error \
    -ss 0 -t 4 \
    -i "downloads/${source}.webm" \
    -vf "scale=900:720:force_original_aspect_ratio=decrease,pad=900:720:(ow-iw)/2:(oh-ih)/2:color=151a20,fps=24" \
    -an -movflags +faststart -pix_fmt yuv420p \
    "assets/${slug}.mp4"
}

prepare_audio() {
  local source="$1"
  local slug="$2"
  ffmpeg -y -loglevel error \
    -i "downloads/${source}.ogg" \
    -t 4 -ac 1 -ar 44100 \
    "assets/${slug}.wav"
}

prepare_image r3-china-shanghai
prepare_image r3-japan-osaka
prepare_image r3-china-calligraphy
prepare_image r3-japan-calligraphy
prepare_image r3-china-panda
prepare_image r3-japan-macaque
prepare_image r3-china-garden
prepare_image r3-japan-kyoto

prepare_video r3-china-video r3-china-video
prepare_video r3-japan-video r3-japan-video

prepare_audio r3-china-audio r3-china-audio
prepare_audio r3-japan-audio r3-japan-audio
