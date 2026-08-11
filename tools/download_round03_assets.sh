#!/usr/bin/env bash
set -euo pipefail

mkdir -p downloads sources

download() {
  local out="$1"
  local url="$2"
  curl_chrome145 -L -s -o "$out" "$url"
}

commons_file() {
  local name="$1"
  printf 'https://commons.wikimedia.org/wiki/Special:Redirect/file/%s' "$name"
}

download downloads/r3-china-shanghai.jpg "$(commons_file 'Shanghai_skyline_from_the_bund.jpg?width=1280')"
download downloads/r3-japan-osaka.jpg "$(commons_file 'Osaka_castle.jpg?width=1280')"
download downloads/r3-china-calligraphy.jpg "$(commons_file 'Chinese_Calligraphy_%2828492621438%29.jpg?width=1280')"
download downloads/r3-japan-calligraphy.jpg "$(commons_file 'Japanese_calligraphy.jpg?width=1280')"
download downloads/r3-china-panda.jpg "$(commons_file 'Young_Chengdu_panda.jpg?width=1280')"
download downloads/r3-japan-macaque.jpg "$(commons_file 'Japanese_macaque.jpg?width=1280')"
download downloads/r3-china-garden.jpg "$(commons_file 'Chinese_garden.jpg?width=1280')"
download downloads/r3-japan-kyoto.jpg "$(commons_file 'Kyoto_Skyline.jpg?width=1280')"

download downloads/r3-china-video.webm "$(commons_file 'Shanghai_Demonstration_%281946%29.webm')"
download downloads/r3-japan-video.webm "$(commons_file 'Japanese_Tea_Garden.webm')"

download downloads/r3-china-audio.ogg "$(commons_file 'Chinese_Vocal_and_Instrumental_Ensemble.ogg')"
download downloads/r3-japan-audio.ogg "$(commons_file 'Shakuhachi-flute-440Hz.ogg')"

cat > sources/round-03-media-sources.md <<'EOF'
# Round 03 Media Sources

- r3-china-shanghai: https://commons.wikimedia.org/wiki/File:Shanghai_skyline_from_the_bund.jpg
- r3-japan-osaka: https://commons.wikimedia.org/wiki/File:Osaka_castle.jpg
- r3-china-calligraphy: https://commons.wikimedia.org/wiki/File:Chinese_Calligraphy_(28492621438).jpg
- r3-japan-calligraphy: https://commons.wikimedia.org/wiki/File:Japanese_calligraphy.jpg
- r3-china-panda: https://commons.wikimedia.org/wiki/File:Young_Chengdu_panda.jpg
- r3-japan-macaque: https://commons.wikimedia.org/wiki/File:Japanese_macaque.jpg
- r3-china-garden: https://commons.wikimedia.org/wiki/File:Chinese_garden.jpg
- r3-japan-kyoto: https://commons.wikimedia.org/wiki/File:Kyoto_Skyline.jpg
- r3-china-video: https://commons.wikimedia.org/wiki/File:Shanghai_Demonstration_(1946).webm
- r3-japan-video: https://commons.wikimedia.org/wiki/File:Japanese_Tea_Garden.webm
- r3-china-audio: https://commons.wikimedia.org/wiki/File:Chinese_Vocal_and_Instrumental_Ensemble.ogg
- r3-japan-audio: https://commons.wikimedia.org/wiki/File:Shakuhachi-flute-440Hz.ogg
EOF
