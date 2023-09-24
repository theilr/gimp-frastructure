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

#  Wrap the G'MIC Paint Daub filter with a scale/rescale
#  so that a greater range of swirl sizes are available

from gimpfu import *
import process

def wrapped_paint_daub(img,layer,f_scale,
                       n_it,amp,sharp,aniso,sigma,di,eql,plasma,p_scale):
    '''wrap GMIC paint daub'''
    with process.UndoContext(img):
        pd_layer = process.visible_base(img,name="PaintDaub")
        wold = pd_layer.width
        hold = pd_layer.height
        wnew = wold * f_scale // 100
        hnew = hold * f_scale // 100
        pdb.gimp_layer_scale(pd_layer,wnew,hnew,0)
        cmd = ('samj_Barbouillage_Paint_Daub '
               '%d,%d,%d,%.1f,%.1f,%.1f,%d,%d,%d'
               % (n_it,amp,sharp,aniso,sigma,di,int(eql),plasma,p_scale))
        print('cmd=',cmd)
        pdb.plug_in_gmic_qt(img,layer,1,0,cmd)
        pdb.gimp_layer_scale(pd_layer,wold,hold,0)


process.pfreg(wrapped_paint_daub,
              [
                  (PF_IMAGE, "image", "Input image", None),
                  (PF_DRAWABLE, "drawable", "Input drawable", None),
                  (PF_SLIDER, "f_scale", "Scale factor (percent)",
                   100, (5, 200, 1)),
                  (PF_SLIDER, "n_it", "Iterations (1-3)", 2, (1,5,1)),
                  (PF_SLIDER, "amp", "Amplitude", 2, (1,5,1)),
                  (PF_SLIDER, "sharp","Sharpness", 100, (0, 500, 1)),
                  (PF_FLOAT, "aniso","Anisotropy (0-1)", 0.2),
                  (PF_FLOAT, "sigma","Sigma (0-5)",1),
                  (PF_FLOAT, "di","DI (0-10)",4),
                  (PF_BOOL, "eql", "Equalize", True),
                  (PF_OPTION, "plasma", "Plasma", 0,
                   ("Non/Without", "Colors A", "Colors B")),
                  (PF_SLIDER, "p_scale", "Scale Plasma", 8, (1,30,1)),
              ],
              name="Wrap Daub",
              description="Wrap GMIC Paint Daub",
              author="theilr",
              year=2023,
              menu="<Image>/Filters/theilr"
)

main()
