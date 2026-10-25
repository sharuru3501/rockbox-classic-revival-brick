# Third-party material and licences

| What | Where it comes from | Licence | In this repository? |
|---|---|---|---|
| Rockbox (source patched by `patches/`) | https://github.com/IncognitoMan/rockbox (fork of https://www.rockbox.org) | GPL-2.0-or-later | No - only a patch |
| "Classic Revival" theme, which `theme/` converts to 640x480 | Doug Belshaw, https://themes.rockbox.org (theme id 4212) | CC BY-SA 4.0 (based on iClassic 1.1 by Humberto Santana, CC BY-SA 3.0) | No - download it yourself; the scripts regenerate the 640x480 version |
| Noto Sans CJK (used to generate the CJK bitmap fonts) | Google / Adobe, Debian package `fonts-noto-cjk` | SIL Open Font License 1.1 | No - generated locally by `theme/make_fonts.sh` |
| PortMaster launcher (`Rockbox.sh`) | `packaging/retro-handheld/` of the Rockbox fork above | GPL-2.0-or-later (ships with the fork's `rockbox_gplv2.txt`) | No - only a small diff (`device/`) |
| Screenshots in `docs/images/` | They show the converted Classic Revival theme | CC BY-SA 4.0, credit: Doug Belshaw (Classic Revival), Humberto Santana (iClassic) | Yes - **these two images are CC BY-SA 4.0, not GPL** |

A theme converted with these scripts is a derivative of "Classic Revival" and must be shared under
CC BY-SA 4.0 with attribution. Generated fonts are derived from Noto Sans CJK (OFL 1.1).

No music, album artwork or personal data is included.

`theme/scale.py` replaces the on-screen label of the original theme (the player name of the device it imitates) with "Rockbox"; credit comments in the skin files are kept.
