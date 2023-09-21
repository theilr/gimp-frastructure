#!/usr/bin/env python
# GIMP Python plug-in for Cheap HDR

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at http://www.gnu.org/licenses for
# more details.

## Note: CheapHDR is applied to the current layer
## May prefer to have it apply to the current visible image

from gimpfu import *
import process

def cheap_hdr(img,layer,radius,spread,opacity):
    with process.UndoContext(img):
        process.cheap_hdr(img,layer,radius,spread,opacity)


process.pfreg(cheap_hdr,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_SLIDER, "radius", "Radius", 500, (0, 1500, 10)),
                  (PF_SLIDER, "spread", "Spread", 50, (0, 250, 10)),
                  (PF_SLIDER, "opacity", "Factor", 50, (0, 100, 5)),
              ],
              name="Cheap HDR",
              description="Reduce global contrast while keeping local contrast",
              author="theilr",
              year=2022,
              menu="<Image>/Filters/theilr",
)

main()
