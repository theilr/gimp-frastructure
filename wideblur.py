#!/usr/bin/env python
# GIMP Python plug-in to allow smoothing by >500 pixels

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at http://www.gnu.org/licenses for
# more details.


from gimpfu import *
import process

def wide_blur(img, layer, radius):
    with process.UndoContext(img):
        process.wide_blur(img,layer,radius)

process.pfreg(wide_blur,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_SLIDER, "raidus", "Radius", 500, (0,1500,10))
              ],
              name="Wide blur",
              description="Gaussian blur of possibly large radii",
              author="theilr",
              year=2022,
              menu="<Image>/Filters/theilr"
)

main()
