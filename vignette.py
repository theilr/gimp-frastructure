#!/usr/bin/env python
# GIMP Python plug-in to produce a jagged border around the image

DESCRIPTION='''Darkens the corners in a soft way

USAGE NOTES:  Since this non-destructively produces an overlay layer
you can make tweaks to the effect.
'''

from gimpfu import *
import process

def vignette(img,layer,lighten_corners,blur_radius,opacity,noise_spread):
    with process.UndoContext(img):
        process.vignette(img,layer,lighten_corners,blur_radius,opacity,noise_spread)

process.pfreg(vignette,
              [
                  (PF_IMAGE, "img", "Input image", None),
                  (PF_LAYER, "layer", "Input layer", None),
                  (PF_OPTION, "lighten_corners", "Corners", 0,
                   ("Darken", "Lighten")),
                  (PF_SLIDER, "blur_radius", "Blur", 500, (50,2500,50)),
                  (PF_SLIDER, "opacity", "Opacity", 50, (0, 100, 1)),
                  (PF_BOOL, "noise_spread", "Spread noise", True),
              ],
              name="Vignette",
              description=DESCRIPTION,
              author="theilr",
              year="2022",
              menu="<Image>/Filters/theilr"
)

main()
