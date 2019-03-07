import sys
import os
import gc
import argparse
from openslide import OpenSlide


parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('-l', '--level', type=int, default=0)
parser.add_argument('-s', '--size', type=int, default=10000)
args = parser.parse_args()

SRC_PATH = args.path
LEVEL = args.level
SIZE = args.size

SRC_NAME, _ = os.path.splitext(os.path.basename(SRC_PATH))
DST_DIR = f'./outputs/{SRC_NAME}/{LEVEL}'
os.makedirs(DST_DIR, exist_ok=True)
s = OpenSlide(SRC_PATH)
dims = s.level_dimensions[LEVEL]
W, H = dims[:2]
X = W // SIZE + 1
Y = H // SIZE + 1
ww = [(W + i) // X for i in range(X)]
hh = [(H + i) // Y for i in range(Y)]

print(f' {dims} pixels {X} / {Y} tiles')
downsamples = s.level_downsamples[LEVEL]
pos = [0, 0]
for y, h in enumerate(hh):
    pos[0] = 0
    for x, w in enumerate(ww):
        img = s.read_region(pos, LEVEL, (w, h))
        # if not img.mode == 'RGB':
        #   img = img.convert('RGB')
        # img.save(f'{DST_DIR}/{x}_{y}_tile.jpg', quality=100, optimize=True)
        print(pos, x, y, w, h, img.mode)
        img.close()
        pos[0] += w
    pos[1] += h
    gc.collect()

print('done')
