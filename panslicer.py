#!/usr/bin/python
#
# panslicer slices huge images in tiles suitable for use with leaflet
# and possibly other software
#
# Copyright (C) 2012 Christian Franke <nobody-panslicer@nowhere.ws>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
import sys
import os
from PIL import Image

if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: %s <image>" % sys.argv[0]
    sys.exit(1)

img = Image.open(sys.argv[1])
size = img.size
tile_size = 256

# Use width
idx = 1

# Image width should be tile_size times a power of two
scale = (tile_size * (2 ** (math.ceil(math.log(float(size[idx])/tile_size,2)))))/size[idx]
size = (int(round(size[0] * scale)), int(round(size[1] * scale)))

# Resize image to the calculated size
print >>sys.stderr, "Scaling up image to a suitable size"
img = img.resize(size, Image.ANTIALIAS)

# Initialize zoom level - we will half the image this many times
zoom = int(math.log(size[idx]/tile_size, 2))

os.mkdir('tiles')
while True:
    os.mkdir('tiles/%d' % zoom)
    for x in range(0, int(math.ceil(float(size[0]) / tile_size))):
        os.mkdir('tiles/%d/%d' % (zoom, x))
        for y in range(0, int(math.ceil(float(size[1]) / tile_size))):
            tile_box = (
                x * tile_size,
                y * tile_size,
                (x+1) * tile_size,
                (y+1) * tile_size
            )

            tile_file = 'tiles/%d/%d/%d.jpg' % (zoom, x, y)
            print >>sys.stderr, "Creating %s" % tile_file
            img.crop(tile_box).save(tile_file, quality=95, optimize=True)
    if zoom == 0:
        break
    zoom = zoom - 1
    size = (int(0.5*size[0]), int(0.5*size[1]))
    print >>sys.stderr, "Halfing image as we go to zoom level %d" % zoom
    img = img.resize(size, Image.ANTIALIAS)
