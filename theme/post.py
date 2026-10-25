import sys, re
from PIL import Image
d = sys.argv[1]                      # h640 directory
wp = d + '/wps/Classic Revival/'
bg = Image.open(wp + 'ClassicRevival_bg.bmp').convert('RGB')
box = (14, 78, 302, 410)             # the art viewport (x, y, x+w, y+h)
bg.crop(box).save(wp + 'NoArt.bmp', 'BMP')       # placeholder + reflection, shown only without cover art
bg.paste((255, 255, 255), box)
bg.save(wp + 'ClassicRevival_bg.bmp', 'BMP')
p = d + '/wps/Classic Revival.wps'
t = open(p, encoding='utf-8').read()
t = t.replace('%xl(w,FrameTop.bmp,0,0)\n%xl(x,FrameLeft.bmp,0,26)\n%xl(y,FrameRight.bmp,280,26)\n%xl(z,FrameBottom.bmp,0,272)\n', '%xl(N,NoArt.bmp,0,0)\n')
t = t.replace('%Cl(6,8,276,276,c,c)', '%Cl(6,8,276,276,c,c,p)')
t = t.replace('%V(14,78,288,284,-)', '%V(14,78,288,332,-)')
t = t.replace('%Cd%?C<%xd(w)%xd(x)%xd(y)%xd(z)|>', '%Cd%?C<|%xd(N)>')
open(p, 'w', encoding='utf-8').write(t)
print('post ok', 'xd(N)' in t, ',c,c,p)' in t)
