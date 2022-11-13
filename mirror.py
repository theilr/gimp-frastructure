#!/usr/bin/env python
# GIMP Python plug-in to make mirrors, hemitropes, and quadrupoles

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

def mirror(img, layer, m_horiz, m_vert, ul_hflip, ul_vflip):
    with process.UndoContext(img):
        process.mirror(img, layer, m_horiz, m_vert, ul_hflip, ul_vflip)

process.pfreg(mirror,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_BOOL, "m_horiz", "Horizontal mirror", True),
                  (PF_BOOL, "m_vert", "Vertical mirror", True),
                  (PF_BOOL, "ul_hflip", "Horiz flip upper-left", False),
                  (PF_BOOL, "ul_vflip", "Vert flip upper left", False),
              ],
              name="Mirror",
              description="Reflect an image (possibly multiple times)",
              author="theilr",
              year=2022,
              menu="<Image>/Filters/theilr"
)

main()
