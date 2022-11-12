#!/usr/bin/env python
# GIMP Python plug-in to make mirrors, hemitropes, and quadrupoles

from gimpfu import *
import process

def accordion(img, layer, n_horiz, n_vert, do_flip, ul_hflip, ul_vflip):
    with process.UndoContext(img):
        process.accordion(img, layer,
                          int(n_horiz), int(n_vert), ## PF_SPINNER not int's
                          do_flip,ul_hflip, ul_vflip)

process.pfreg(accordion,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_SPINNER, "n_horiz", "Horizontal accordion", 2, (1,10,1)),
                  (PF_SPINNER, "n_vert", "Vertical accordion", 2, (1,10,1)),
                  (PF_BOOL, "do_flip", "Mirror adjacent tiles", True),
                  (PF_BOOL, "ul_hflip", "Horiz flip upper-left", False),
                  (PF_BOOL, "ul_vflip", "Vert flip upper left", False),
              ],
              name="Accordion",
              description="Folds/mirros an image (possibly multiple times)",
              author="theilr",
              year=2022,
              menu="<Image>/Filters/theilr"
)

main()
