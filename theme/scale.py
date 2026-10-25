import re, sys, os, shutil
from PIL import Image
K = 2
src = sys.argv[1]   # .../x/.rockbox
dst = sys.argv[2]
FONT_MAP = {   # replaced later by the real generated fonts
    '14-Sazanami-Mincho.fnt': 'CR-28.fnt',
    '16-GNU-Unifont.fnt': 'CR-32.fnt',
    '24-ClassicRevival-Spacer.fnt': '48-ClassicRevival-Spacer.fnt',
}
def sc(v):
    v = v.strip()
    if re.fullmatch(r'-?\d+', v):
        return str(int(v) * K)
    return v
def scale_args(args, idxs):
    out = list(args)
    for i in idxs:
        if i < len(out): out[i] = sc(out[i])
    return out
# tag -> indexes of numeric args to scale
TAGS = {
  'T': [0,1,2,3],
  'V': [0,1,2,3],
  'Vl': [1,2,3,4], 'Vi': [1,2,3,4],
  'xl': [2,3],
  'Cl': [0,1,2,3],
  'Lb': [1,2],
  'LB': [0,1,2,3],
  'pb': [0,1,2,3], 'pv': [0,1,2,3],
}
pat = re.compile(r'%(T|Vl|Vi|V|xl|Cl|Lb|LB|pb|pv)\(([^()]*)\)')
CUR = {'ext': ''}
MINH = {'1': 36, '2': 32, '3': 36}   # text viewport heights (font id -> minimum height)
def repl(m):
    tag, body = m.group(1), m.group(2)
    args = body.split(',')
    args = scale_args(args, TAGS[tag])
    if tag in ('V', 'Vl'):
        o = 1 if tag != 'V' else 0
        if len(args) > o + 4:
            font = args[o + 4].strip()
            if font in MINH and not (font == '3' and CUR['ext'] == '.sbs'):
                try:
                    y = int(args[o + 1]); h = int(args[o + 3])
                    if h < MINH[font]:
                        d = MINH[font] - h
                        ny = max(0, y - d // 2)
                        if ny + h + d > 480: ny = 480 - (h + d)
                        args[o + 1] = str(ny); args[o + 3] = str(h + d)
                except ValueError:
                    pass
    return '%' + tag + '(' + ','.join(args) + ')'
def fix_fonts(t):
    for a, b in FONT_MAP.items(): t = t.replace(a, b)
    return t
os.makedirs(dst, exist_ok=True)
for root, dirs, files in os.walk(src):
    rel = os.path.relpath(root, src)
    od = os.path.join(dst, rel)
    os.makedirs(od, exist_ok=True)
    for f in files:
        p = os.path.join(root, f); q = os.path.join(od, f)
        if f.endswith(('.wps', '.sbs', '.fms')):
            CUR['ext'] = os.path.splitext(f)[1]
            t = open(p, encoding='utf-8').read()
            # on-screen labels: use "Rockbox" instead of the trademarked player name (comments keep the credits)
            t = '\n'.join(l if l.startswith('#') else pat.sub(repl, l).replace('iPod', 'Rockbox') for l in t.split('\n'))
            if f.endswith('.sbs'):
                t = re.sub(r'%Vl\((s|f|m),(\d+),10,(\d+),30,-\)%Vg\(599AD7,2677C3,FFFFFF\)', r'%Vl(\1,\2,6,\3,36,-)%Vg(619FDA,2274C1,FFFFFF)', t)
            open(q, 'w', encoding='utf-8').write(fix_fonts(t))
        elif f.endswith('.cfg'):
            open(q, 'w', encoding='utf-8').write(open(p, encoding='utf-8').read())
        elif f.endswith('.bmp'):
            im = Image.open(p).convert('RGB')
            has_key = any(px == (255, 0, 255) for px in im.getdata())
            res = Image.NEAREST if has_key else Image.LANCZOS
            im.resize((im.width * K, im.height * K), res).save(q, 'BMP')
        elif f.endswith('.fnt'):
            pass
        else:
            shutil.copy(p, q)
print('done')
