#!/usr/bin/env python
# GIMP Python plug-in to produce a jagged border around the image

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at http://www.gnu.org/licenses for
# more details.


DESCRIPTION='''
Creates a white (or black) border around an image that merges in with
the image so that on a larger white (or black) background, the image
appears to have a ragged border.  This is similar to the Gimp's Fuzzy
Border, but it adapts its jaggedness to the image. (Also unlike Fuzzy
Border, it is deterministic, it does not depend on random number
seeds.)

USAGE NOTES: Since this non-destructively produces a border as a
separate layer, you can tweak the border; eg smooth it (yuck, then it's
not very jagged anymore!), change its color, use it to build some
fancy drop-shadow, etc.  A number of effects can be obtained by using
the white/black border layer and/or its inverse as a layer mask.
'''

from gimpfu import *
import process

def jagged_border(img,layer,border_shape,black_border,border_size,
                  thresh,fill_islands,one_pixel_border):
    with process.UndoContext(img):
        process.jagged_border(img,layer,border_shape,black_border,border_size,
                              thresh,fill_islands,one_pixel_border)

process.pfreg(jagged_border,
              [
                  (PF_IMAGE, "img", "Input image", None),
                  (PF_LAYER, "layer", "Input layer", None),
                  (PF_OPTION, "border_shape", "Border shape", 0,
                   ("Rectangular",
                    "Horizontal only",
                    "Vertical only",
                    "Elliptical",
                    "Rounded Rectangular",
                   )
                  ),
                  (PF_OPTION, "black_border", "Border Color", 0,
                   ("Black", "White")),
                  (PF_SLIDER, "border_size", "Border width", 50, (5, 1000, 5)),
                  (PF_SLIDER, "threshold", "Threshold", 1, (1, 255, 1)),
                  (PF_BOOL, "fill_islands", "Fill in islands", True),
                  (PF_BOOL, "one_pixel_border", "One-pixel border", True),
              ],
              name="Jagged Border",
              description=DESCRIPTION,
              author="theilr",
              year="2022",
              menu="<Image>/Filters/theilr"
)

main()
