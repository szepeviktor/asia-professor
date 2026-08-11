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

download downloads/r2-china-wall.jpg "$(commons_file 'Great_wall_of_china.jpg?width=1280')"
download downloads/r2-japan-fuji.jpg "$(commons_file 'MountFuji.jpg?width=1280')"
download downloads/r2-china-opera.jpg "$(commons_file 'Wang_Mintong_Peking_Opera.jpg?width=1280')"
download downloads/r2-japan-kabuki.jpg "$(commons_file 'Kabuki_Performer.jpg?width=1280')"
download downloads/r2-china-tea.jpg "$(commons_file 'Chinese_Tea_Ceremony.jpg?width=1280')"
download downloads/r2-japan-samurai.jpg "$(commons_file 'SamuraiArmor.jpg?width=1280')"

download downloads/r2-china-video.webm "$(commons_file 'Lion_Dance_2025.webm')"
download downloads/r2-japan-video.webm "$(commons_file 'Japanese_Tea_Garden.webm')"

download downloads/r2-china-audio.ogg "$(commons_file 'Fanyin.ogg')"
download downloads/r2-japan-audio.ogg "$(commons_file 'Shamisenwithvocals_2006.ogg')"

cat > sources/round-02-media-sources.md <<'EOF'
# Round 02 Media Sources

- r2-china-wall: https://commons.wikimedia.org/wiki/File:Great_wall_of_china.jpg
- r2-japan-fuji: https://commons.wikimedia.org/wiki/File:MountFuji.jpg
- r2-china-opera: https://commons.wikimedia.org/wiki/File:Wang_Mintong_Peking_Opera.jpg
- r2-japan-kabuki: https://commons.wikimedia.org/wiki/File:Kabuki_Performer.jpg
- r2-china-tea: https://commons.wikimedia.org/wiki/File:Chinese_Tea_Ceremony.jpg
- r2-japan-samurai: https://commons.wikimedia.org/wiki/File:SamuraiArmor.jpg
- r2-china-video: https://commons.wikimedia.org/wiki/File:Lion_Dance_2025.webm
- r2-japan-video: https://commons.wikimedia.org/wiki/File:Japanese_Tea_Garden.webm
- r2-china-audio: https://commons.wikimedia.org/wiki/File:Fanyin.ogg
- r2-japan-audio: https://commons.wikimedia.org/wiki/File:Shamisenwithvocals_2006.ogg
EOF
