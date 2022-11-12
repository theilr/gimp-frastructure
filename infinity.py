#!/usr/bin/env python
# GIMP Python plug-in to "bend" a panorama image into a rainbow shape

# NOTE: This is very similar in purpose to the 'arclayer.py' plug-in
# written by Akkana Peck (2002) http://www.shallowsky.com/software/

DESCRIPTION='''
Builds from Pan to Bow: takes an image, and bends it into both
rainbow and smile shapes of 180 degrees.  Then makes flipped copies
of each and from those four components, combines them into a 
figure-8 racetrack that kind of looks like an infinity symbol
'''

from gimpfu import *
import process

def infinity(img,bkg_color):
    with process.UndoContext(img):
        process.infinity(img,bkg_color)

process.pfreg(infinity,
              [
                  (PF_IMAGE, "img", "Input image", None),
                  (PF_COLOR, "bkg_color", "Background color", (1.,1.,0.))
              ],
              name="Infinity",
              description=DESCRIPTION,
              author="theilr",
              year="2022",
              menu="<Image>/Filters/theilr"
)

main()
