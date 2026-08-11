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

prepare_image r2-china-wall
prepare_image r2-japan-fuji
prepare_image r2-china-opera
prepare_image r2-japan-kabuki
prepare_image r2-china-tea
prepare_image r2-japan-samurai

prepare_video r2-china-video r2-china-video
prepare_video r2-japan-video r2-japan-video

prepare_audio r2-china-audio r2-china-audio
prepare_audio r2-japan-audio r2-japan-audio
