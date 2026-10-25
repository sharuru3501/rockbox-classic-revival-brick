#!/bin/bash
# Build the 640x480 version of the "Classic Revival" Rockbox theme.
# usage: build_theme.sh <unzipped original theme: the ".rockbox" folder> <fonts dir with CR-28.fnt CR-32.fnt 48-ClassicRevival-Spacer.fnt> <output dir>
set -e
SRC="$1"; FONTS="$2"; OUT="$3"; HERE="$(cd "$(dirname "$0")" && pwd)"
rm -rf "$OUT"; python3 "$HERE/scale.py" "$SRC" "$OUT"
mkdir -p "$OUT/fonts"; cp "$FONTS"/CR-28.fnt "$FONTS"/CR-32.fnt "$FONTS"/48-ClassicRevival-Spacer.fnt "$OUT/fonts/"
# the port bind-mounts the Rockbox folder at /tmp/rockbox; the theme cfg must point there
sed -i.bak 's#/\.rockbox#/tmp/rockbox#g; s#17-NimbusSans-Bold.fnt#CR-32.fnt#' "$OUT/themes/ClassicRevival.cfg" 2>/dev/null || true
[ -f "$OUT/themes/Classic Revival.cfg" ] && mv "$OUT/themes/Classic Revival.cfg" "$OUT/themes/ClassicRevival.cfg" && sed -i.bak 's#/\.rockbox#/tmp/rockbox#g; s#17-NimbusSans-Bold.fnt#CR-32.fnt#' "$OUT/themes/ClassicRevival.cfg"
rm -f "$OUT"/themes/*.bak
python3 "$HERE/frames.py" "$SRC/wps/Classic Revival" "$OUT/wps/Classic Revival"
python3 "$HERE/pane.py" "$SRC/wps/Classic Revival/Pane.bmp" "$OUT/wps/Classic Revival/Pane.bmp"
python3 "$HERE/post.py" "$OUT"
echo "theme written to $OUT"
