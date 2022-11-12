#!/usr/bin/env python
# GIMP Python plug-in for Cheap HDR
## Note: CheapHDR is applied to the current layer
## May prefer to have it apply to the current visible image

from gimpfu import *
import process

def cheap_hdr(img,layer,radius,opacity):
    with process.UndoContext(img):
        process.cheap_hdr(img,layer,radius,opacity)


process.pfreg(cheap_hdr,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_SLIDER, "radius", "Radius", 500, (0, 1500, 10)),
                  (PF_SLIDER, "opacity", "Factor", 50, (0, 100, 1)),
              ],
              name="Cheap HDR",
              description="Reduce global contrast while keeping local contrast",
              author="theilr",
              year=2022,
              menu="<Image>/Filters/theilr",
)

main()
