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
  local culture="$1"
  local slug="$2"
  ffmpeg -y -loglevel error \
    -ss 0 -t 4 \
    -i "downloads/${culture}-video.webm" \
    -vf "scale=900:720:force_original_aspect_ratio=decrease,pad=900:720:(ow-iw)/2:(oh-ih)/2:color=151a20,fps=24" \
    -an -movflags +faststart -pix_fmt yuv420p \
    "assets/${slug}.mp4"
}

prepare_audio() {
  local culture="$1"
  local slug="$2"
  ffmpeg -y -loglevel error \
    -i "downloads/${culture}-audio.ogg" \
    -t 3 -ac 1 -ar 44100 \
    "assets/${slug}.wav"
}

slugs=(
  china-clothes
  japan-clothes
  china-music
  japan-music
  china-food
  japan-food
  china-festival
  japan-festival
  china-building
  japan-building
)

for slug in "${slugs[@]}"; do
  prepare_image "$slug"
  culture="${slug%%-*}"
  prepare_video "$culture" "$slug"
  prepare_audio "$culture" "$slug"
done
