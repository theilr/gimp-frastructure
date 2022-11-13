#!/usr/bin/env python
# GIMP Python plug-in to "bend" a panorama image into a rainbow shape

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at http://www.gnu.org/licenses for
# more details.


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

def infinity(img,bkg_color,pad,squeeze):
    with process.UndoContext(img):
        process.infinity(img,bkg_color,pad,int(squeeze))

process.pfreg(infinity,
              [
                  (PF_IMAGE, "img", "Input image", None),
                  (PF_COLOR, "bkg_color", "Background color", (1.,1.,1.)),
                  (PF_SPINNER, "pad", "Pad angle", 0, (0, 270, 15)),
                  (PF_BOOL, "squeeze", "Squeeze middle", False),
              ],
              name="Pan to Infinity",
              description=DESCRIPTION,
              author="theilr",
              year="2022",
              menu="<Image>/Filters/theilr"
)

main()
