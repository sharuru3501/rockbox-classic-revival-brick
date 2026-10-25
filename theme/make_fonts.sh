#!/bin/bash
# Generate the CJK bitmap fonts (Rockbox .fnt) from Noto Sans CJK Bold with Rockbox's convttf,
# inside an arm64 Debian 11 container. usage: make_fonts.sh <rockbox source dir> <output dir>
set -e
SRC="$(cd "$1" && pwd)"; OUT="$(mkdir -p "$2" && cd "$2" && pwd)"
docker run --rm --platform linux/arm64 -v "$SRC":/src:ro -v "$OUT":/out debian:bullseye bash -c '
printf "deb http://archive.debian.org/debian bullseye main\ndeb http://archive.debian.org/debian-security bullseye-security main\n" > /etc/apt/sources.list
rm -f /etc/apt/sources.list.d/*
apt-get -o Acquire::Check-Valid-Until=false update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq gcc libfreetype6-dev fonts-noto-cjk >/dev/null 2>&1
gcc -O2 -I/usr/include/freetype2 -o /tmp/convttf /src/tools/convttf.c -lfreetype -lm
gcc -O2 -o /tmp/convbdf /src/tools/convbdf.c
cd /out; F=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
/tmp/convttf -s 32 -l 40959 -p 26 -Ta 3 -Td 1 -o CR-28.fnt $F >/dev/null
/tmp/convttf -s 32 -l 40959 -p 30 -Ta 3 -Td 1 -o CR-32.fnt $F >/dev/null
{ echo "STARTFONT 2.1"; echo "FONT -spacer-48"; echo "SIZE 48 75 75"; echo "FONTBOUNDINGBOX 1 48 0 0"
  echo "STARTPROPERTIES 2"; echo "FONT_ASCENT 48"; echo "FONT_DESCENT 0"; echo "ENDPROPERTIES"; echo "CHARS 1"
  echo "STARTCHAR space"; echo "ENCODING 32"; echo "SWIDTH 1 0"; echo "DWIDTH 1 0"; echo "BBX 1 48 0 0"; echo "BITMAP"
  for i in $(seq 48); do echo 00; done; echo "ENDCHAR"; echo "ENDFONT"; } > sp.bdf
/tmp/convbdf -f -o 48-ClassicRevival-Spacer.fnt sp.bdf; rm sp.bdf
ls -la /out'
