import sys
import os
import gc
from openslide import OpenSlide

if len(sys.argv) < 2:
    print('Invalid arguments.')
    exit(1)

SRC_PATH = sys.argv[1]
LEVEL = 0 if (len(sys.argv) < 3) else int(sys.argv[2])
TILE_SIZE = 10000

SRC_NAME, _ = os.path.splitext(os.path.basename(SRC_PATH))
DST_DIR = f'./outputs/{SRC_NAME}_{LEVEL}'

os.makedirs(DST_DIR, exist_ok=True)
s = OpenSlide(SRC_PATH)
dims = s. level_dimensions[LEVEL]
W = dims[0]
H = dims[1]
X = int(W / TILE_SIZE) + 1
Y = int(H / TILE_SIZE) + 1
print(f' {dims} pixels {X} / {Y} tiles')
for x in range(0, X):
    for y in range(0, Y):
        w = TILE_SIZE if (x < X - 1) else W % TILE_SIZE
        h = TILE_SIZE if (y < Y - 1) else H % TILE_SIZE
        img = s.read_region((x * TILE_SIZE, y * TILE_SIZE), LEVEL, (w, h))
        if not img.mode == 'RGB':
          img = img.convert('RGB')
        img.save(f'{DST_DIR}/{x}_{y}_tile.jpg', quality=100, optimize=True)
        img.close()
        print(f'{x} / {y} saved')
    gc.collect()

print('done')
