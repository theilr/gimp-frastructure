#!/usr/bin/env python
# GIMP Python plug-in to scale image to fibonacci size

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
Converts a square image into a Fibonacci spiral with many
copies of the image arranged in a spiral pattern in a
golden rectangle.
'''

from gimpfu import *
import process

def fibonacci_spiral(img,aspect,q_turn,blend,opacity,merge_down):
    with process.UndoContext(img):
        process.fibonacci_spiral(img,aspect,q_turn,blend,opacity,merge_down)

process.pfreg(fibonacci_spiral,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_OPTION, "aspect", "Aspect", 1,
                   ("Rectangle", "Square")),
                  (PF_OPTION, "q_turn", "Rotate", 1,
                   ("No Rotation",
                    "90 degrees (CW)",
                    "180 degrees",
                    "270 degrees (CCW)")),
                  (PF_RADIO, "blend", "Blend Mode:", LAYER_MODE_NORMAL,
                   (("Normal", LAYER_MODE_NORMAL),
                    ("Overlay", LAYER_MODE_OVERLAY),
                    ("Multiply", LAYER_MODE_MULTIPLY),
                    ("Add", LAYER_MODE_ADDITION),
                    ("Darken", LAYER_MODE_DARKEN_ONLY),
                    ("Lighten", LAYER_MODE_LIGHTEN_ONLY),
                    ("Dodge", LAYER_MODE_DODGE),
                    ("Burn", LAYER_MODE_BURN),
                    )),
                  (PF_SLIDER, "opacity", "Opacity", 100, (0, 100, 1)),
                  (PF_BOOL, "merge_down", "Merge Layers", False),
              ],
              name="Fibonacci Spiral...",
              description=DESCRIPTION,
              author="theilr",
              year="2009-2022",
              menu="<Image>/Filters/theilr"
)

main()
