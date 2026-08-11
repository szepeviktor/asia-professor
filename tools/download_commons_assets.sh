#!/usr/bin/env bash
set -euo pipefail

mkdir -p downloads assets sources

download() {
  local out="$1"
  local url="$2"
  curl_chrome145 -L -s -o "$out" "$url"
}

commons_file() {
  local name="$1"
  printf 'https://commons.wikimedia.org/wiki/Special:Redirect/file/%s' "$name"
}

download downloads/china-clothes.jpg "$(commons_file 'A_Cantonese_woman_in_Hanfu.jpg?width=1280')"
download downloads/japan-clothes.jpg "$(commons_file 'Japanese_Kimono.jpg?width=1280')"
download downloads/china-music.jpg "$(commons_file 'Guqin.jpg?width=1280')"
download downloads/japan-music.jpg "$(commons_file 'Taiko_drum.jpg?width=1280')"
download downloads/china-food.jpg "$(commons_file 'Jiaozi.jpg?width=1280')"
download downloads/japan-food.jpg "$(commons_file 'SUSHI.jpg?width=1280')"
download downloads/china-festival.jpg "$(commons_file 'Chinese_lanterns.jpg?width=1280')"
download downloads/japan-festival.jpg "$(commons_file 'Koinobori.jpg?width=1280')"
download downloads/china-building.jpg "$(commons_file 'Forbidden_City_Beijing_China.jpg?width=1280')"
download downloads/japan-building.jpg "$(commons_file 'Fushimi-Inari.jpg?width=1280')"

download downloads/china-video.webm "$(commons_file 'Chinese-new-year-dragon.webm')"
download downloads/japan-video.webm "$(commons_file 'Sanja_Matsuri.webm')"

download downloads/china-audio.ogg "$(commons_file 'China_cymbal_music.ogg')"
download downloads/japan-audio.ogg "$(commons_file '02_Taiko2_%28short%29.oga')"

cat > sources/media-sources.md <<'EOF'
# Media Sources

- china-clothes: https://commons.wikimedia.org/wiki/File:A_Cantonese_woman_in_Hanfu.jpg
- japan-clothes: https://commons.wikimedia.org/wiki/File:Japanese_Kimono.jpg
- china-music: https://commons.wikimedia.org/wiki/File:Guqin.jpg
- japan-music: https://commons.wikimedia.org/wiki/File:Taiko_drum.jpg
- china-food: https://commons.wikimedia.org/wiki/File:Jiaozi.jpg
- japan-food: https://commons.wikimedia.org/wiki/File:SUSHI.jpg
- china-festival: https://commons.wikimedia.org/wiki/File:Chinese_lanterns.jpg
- japan-festival: https://commons.wikimedia.org/wiki/File:Koinobori.jpg
- china-building: https://commons.wikimedia.org/wiki/File:Forbidden_City_Beijing_China.jpg
- japan-building: https://commons.wikimedia.org/wiki/File:Fushimi-Inari.jpg
- china-video: https://commons.wikimedia.org/wiki/File:Chinese-new-year-dragon.webm
- japan-video: https://commons.wikimedia.org/wiki/File:Sanja_Matsuri.webm
- china-audio: https://commons.wikimedia.org/wiki/File:China_cymbal_music.ogg
- japan-audio: https://commons.wikimedia.org/wiki/File:02_Taiko2.ogg_(short).ogg
EOF
