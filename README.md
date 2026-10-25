# Rockbox Classic Revival for TrimUI Brick (Knulli)

Rockbox + the "Classic Revival" theme, optimised for the TrimUI Brick: 640x480 rendering, large CJK-capable
fonts and a perspective cover-art "Now Playing" screen.

A patch and a set of scripts that run the PortMaster build of Rockbox
([IncognitoMan/rockbox](https://github.com/IncognitoMan/rockbox)) at **640x480** instead of 320x240 on a
TrimUI Brick running Knulli (1024x768 panel, shown at 1.6x), with a click-wheel-player
style "Now Playing" screen (the look of the Classic Revival theme): the cover art is turned in
perspective, with a reflection and anti-aliased edges.

TrimUI Brick + Knulli で Rockbox (PortMaster 版) を 640x480 で描画し、テーマ「Classic Revival」を
Brick 向けに最適化するためのパッチとスクリプトです (ジャケットを奥行き方向に傾け、反射と滑らかな縁を付ける)。

## What is in here

| Path | What |
|---|---|
| `patches/0001-rockbox-hires-perspective-art.patch` | Changes to the Rockbox source (base commit in `patches/BASE_COMMIT.txt`) |
| `theme/` | Scripts that convert the "Classic Revival" theme to 640x480 and generate large CJK fonts |
| `device/` | Small diffs to the PortMaster launcher (`Rockbox.sh`) and `firmware/knulli` |
| `docs/images/` | Screenshots of the UI (menus only, no album art) |

### The Rockbox patch

* `LCD_WIDTH` / `LCD_HEIGHT` of the `retro-handheld` target: 320x240 -> 640x480.
* New optional 7th parameter of the skin tag `%Cl`: `%Cl(x,y,w,h,c,c,p)`.
  With `p` the album art is drawn with a perspective projection (left edge nearest, right edge at 89 %
  height), with a faded reflection below it. Edge pixels are blended with what is already in the
  framebuffer, so the slanted edges are smooth. Only the 24-bit colour LCD path is implemented.
* `lib/skin_parser/tag_table.c`: `%Cl` accepts the extra parameter (without this the whole WPS fails to
  parse and Rockbox falls back to its plain built-in screen).

### The theme

Start from the "Classic Revival" theme (CC BY-SA 4.0, see `NOTICE.md`), then:

```sh
theme/make_fonts.sh <rockbox source dir> fonts_out          # needs Docker; ~10 MB per font
theme/build_theme.sh <unzipped theme>/.rockbox fonts_out out # needs Python 3 with Pillow, numpy, scipy
```

`scale.py` multiplies every coordinate in the skins by 2 and resamples the bitmaps, makes text
viewports tall enough for the CJK fonts, `frames.py`/`pane.py` redraw the art frame and the music-note
pane with anti-aliasing, and `post.py` switches the skin to the new `%Cl(...,p)` drawing and moves the
"no artwork" placeholder into its own bitmap.

### Build and install (summary)

1. Clone `IncognitoMan/rockbox` at the commit in `patches/BASE_COMMIT.txt`, apply the patch.
2. Build in an aarch64 Debian 11 (bullseye) environment as described in the port's `rockbox.md`
   (`tools/configure --target=210 --type=N`, then `make bin`). Games that need 1024x768 bitmaps fail to
   build with a different resolution; they are not needed for music playback (`make -k`).
3. Copy the result next to the original port as a second folder, for example `ports/rockbox-hires/`,
   with a copy of `Rockbox.sh` changed as in `device/Rockbox-HiRes.sh.diff` (it starts the binary with
   `--zoom 1.6`, 640 x 1.6 = 1024). `device/firmware-knulli.diff` ignores the power button while Rockbox
   runs (so the screen can time out without suspending) and asks SDL for smooth scaling.
4. `config.cfg` values used: `volume: -18`, `volume adjustment mode: perceptual`,
   `perceptual volume step count: 40`, `backlight timeout: 180`, plus the theme's own lines.

## Status

Tested on one TrimUI Brick with Knulli (gladiator-ii) and PortMaster 2026.10.24. Not tested elsewhere.
Album art with a non-square aspect ratio has not been checked.

## Licence

GPL-2.0-or-later for the patch, the scripts and the launcher diffs (`LICENSE`). The two screenshots in
`docs/images/` show the Classic Revival theme and are CC BY-SA 4.0 (credit: Doug Belshaw, Humberto Santana).
Other material: see `NOTICE.md`.
The Classic Revival theme imitates the look of Apple's iPod classic. iPod is a trademark of Apple Inc.;
Rockbox and other names belong to their respective owners. This project is not affiliated with or endorsed by
Apple, the Rockbox project, TrimUI or the Knulli project.
