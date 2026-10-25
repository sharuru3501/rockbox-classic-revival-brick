import sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(float)
H, W = a.shape[:2]
K, SS = 2, 8
L = a.mean(axis=2)
big = np.asarray(im.resize((W * K * SS, H * K * SS), Image.BICUBIC)).astype(float)
Lb = gaussian_filter(big.mean(axis=2), 7)
mask_hi = (Lb > 135).astype(float)
mask2 = mask_hi.reshape(H * K, SS, W * K, SS).mean(axis=(1, 3))
m1 = (L > 135).astype(float)
def nconv(img, m, sigma):
    num = np.dstack([gaussian_filter(img[..., c] * m, sigma) for c in range(3)])
    den = gaussian_filter(m, sigma)[..., None]
    out = num / np.maximum(den, 1e-4)
    # where the neighbourhood has no samples, fall back to a wider blur
    return np.where(den > 1e-3, out, img)
fg = nconv(a, m1, 0.8)
bg = nconv(a, 1 - m1, 1.2)
up = lambda x: np.asarray(Image.fromarray(np.clip(x, 0, 255).astype(np.uint8)).resize((W * K, H * K), Image.BICUBIC)).astype(float)
mix = up(fg) * mask2[..., None] + up(bg) * (1 - mask2[..., None])
from scipy.ndimage import binary_dilation
base = np.asarray(im.resize((W * K, H * K), Image.LANCZOS)).astype(float)
w = gaussian_filter(binary_dilation(m1 > 0, iterations=4).astype(float), 1.5)
w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).resize((W * K, H * K), Image.BICUBIC)).astype(float)[..., None] / 255
out = mix * w + base * (1 - w)
Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, 'BMP')
print('ok', out.shape)
