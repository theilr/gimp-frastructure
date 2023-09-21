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

#  Cheap HDR + Unsharp maks + Contrast stretch
#  Quick AND idiosyncratic -- this is just my personal taste

from gimpfu import *
import process

def quick_enhance(img,layer,r_hdr,s_hdr,f_hdr,r_sharp,s_l_mode,f_stretch):
    '''combines cheap-hdr, sharpen, and stretch'''
    with process.UndoContext(img):
        process.cheap_hdr(img,layer,r_hdr,s_hdr,f_hdr)
        process.sharpen(img,layer,r_sharp,s_l_mode)
        if f_stretch:
            process.stretch(img,layer,f_stretch)
        else:
            process.visible_base(img,name="QuickEnhanced")


process.pfreg(quick_enhance,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_SLIDER, "r_hdr", "HDR Radius", 750, (0, 1500, 1)),
                  (PF_SLIDER, "s_hdr", "HDR Spread", 50, (0, 250, 10)),
                  (PF_SLIDER, "f_hdr", "HDR factor", 50, (0, 100, 1)),
                  (PF_SLIDER, "r_sharp", "Unsharp Radius", 9, (0, 25, 1)),
                  (PF_RADIO, "s_l_mode","Sharpen Layer Mode",
                   LAYER_MODE_DARKEN_ONLY,
                   (("darken", LAYER_MODE_DARKEN_ONLY),
                    ("lighten", LAYER_MODE_LIGHTEN_ONLY),
                    ("normal", LAYER_MODE_NORMAL))),
                  (PF_SLIDER, "f_stretch","Stretch factor",50, (0,100,1)),
              ],
              name="Quick Enhance",
              description="Cheap HDR, then sharpen, then stretch",
              author="theilr",
              year=2022,
              menu="<Image>/Filters/theilr"
)

main()
