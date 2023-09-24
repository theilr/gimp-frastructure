#!/usr/bin/env python
# GIMP Python plug-in for a "quick" image enhancement:

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at http://www.gnu.org/licenses for
# more details.

#  Scale Layer to Image size
#  Useful for when you scale a layer to some other size
#  for some kind of processing, and want to scale back

from gimpfu import *
import process

def scale_layer_to_image_size(img,layer):
    '''scale layer to have same size as canvas'''
    with process.UndoContext(img):
        pdb.gimp_layer_scale(layer,img.width,img.height,True)

process.pfreg(scale_layer_to_image_size,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
              ],
              name="Scale Layer to Image",
              description="Scale Layer to Image Size",
              author="theilr",
              year=2023,
              menu="<Image>/Filters/theilr"
)

main()
