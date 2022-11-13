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
Ensures that a rectangular image has pixel counts for height and
width that are successive Fibonacci numbers; and that a square
image has height and width that are the same Fibonacci number.
If not, then the image is rescaled so that the longest dimension
does not increase.
Note, operation is applied to the whole image, not just a layer.
'''

from gimpfu import *
import process

def scale_to_fibonacci(img,squareflag):
    with process.UndoContext(img):
        process.scale_to_fibonacci(img,squareflag)

process.pfreg(scale_to_fibonacci,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_BOOL, "squareflag", "Make square", False),
              ],
              name="Scale to Fibonacci...",
              description=DESCRIPTION,
              author="theilr",
              year="2009-2022",
              menu="<Image>/Filters/theilr"
)

main()
