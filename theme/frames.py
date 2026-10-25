import numpy as np
from PIL import Image
import sys
SRC = sys.argv[1].rstrip('/') + '/'   # original theme's 'wps/Classic Revival/' folder
DST = sys.argv[2].rstrip('/') + '/'
K = 2; SS = 8
KEY = (255, 0, 255)

def load(n):
    im = Image.open(SRC + n).convert('RGB'); return im, np.array(im)

def fill_color(arr, axis_dir):
    """colour image with key pixels replaced by nearest opaque colour along columns"""
    h, w, _ = arr.shape
    key = (arr == KEY).all(axis=2)
    out = arr.copy()
    for x in range(w):
        col = ~key[:, x]
        if not col.any():
            out[:, x] = out[:, max(0, x - 1)] if x else (230, 230, 230); continue
        ys = np.where(col)[0]
        for y in range(h):
            if key[y, x]:
                out[y, x] = arr[ys[np.argmin(abs(ys - y))], x]
    return out

def render(n, kind):
    im, arr = load(n)
    h, w, _ = arr.shape
    key = (arr == KEY).all(axis=2)
    # boundary per column
    xs, bs = [], []
    for x in range(w):
        opaque = np.where(~key[:, x])[0]
        full = len(opaque) == h
        if kind == 'top':
            b = len(opaque)             # rows [0,b) opaque
        else:
            b = h - len(opaque)         # rows [b,h) opaque
        if not full and len(opaque) > 0 and x >= 4:
            xs.append(x + 0.5); bs.append(b)
        elif len(opaque) == 0 and kind == 'bottom' and x >= 4:
            pass
    a, c = np.polyfit(xs, bs, 1)
    # supersampled coverage at K scale
    W, H = w * K, h * K
    ys_ = (np.arange(H * SS) + 0.5) / (K * SS)
    xs_ = (np.arange(W * SS) + 0.5) / (K * SS)
    X, Y = np.meshgrid(xs_, ys_)
    line = a * X + c
    if kind == 'top':
        op = Y < np.clip(line, 0, h)
    else:
        op = Y >= np.clip(line, 0, h)
    # corner columns (x<4) are fully opaque in the original
    op = np.where(X < 4, True, op)
    if kind == 'bottom':
        # columns 4,5 are fully transparent in the original (gap)
        op = np.where((X >= 4) & (X < 6), False, op)
    cov = op.reshape(H, SS, W, SS).mean(axis=(1, 3))
    col = fill_color(arr, 0)
    big = Image.fromarray(col).resize((W, H), Image.BICUBIC)
    # Rockbox's 24-bit LCD ignores bitmap alpha, so pre-blend the edge pixels against a neutral
    # mid grey (a typical cover colour) and keep a magenta colour key for the fully clear area.
    ASSUME = np.array([105.0, 110.0, 115.0])
    rgb = np.array(big).astype(float)
    cv = cov[..., None]
    out = rgb * cv + ASSUME * (1 - cv)
    out = np.where(cv < 0.04, np.array([255.0, 0.0, 255.0]), out)
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8), 'RGB')

for n, kind in (('FrameTop.bmp', 'top'), ('FrameBottom.bmp', 'bottom')):
    img = render(n, kind)
    img.save(DST + n, 'BMP')
    print(n, img.size, img.mode)
# side pieces: solid, no key -> smooth upscale
for n in ('FrameLeft.bmp', 'FrameRight.bmp'):
    im = Image.open(SRC + n).convert('RGB')
    im.resize((im.width * K, im.height * K), Image.BICUBIC).save(DST + n, 'BMP')
    print(n)
