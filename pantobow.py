#!/usr/bin/env python
# GIMP Python plug-in to "bend" a panorama image into a rainbow shape

# NOTE: This is very similar in purpose to the 'arclayer.py' plug-in
# written by Akkana Peck (2002) http://www.shallowsky.com/software/

DESCRIPTION='''
Takes a wide panoramic image and bends it into a rainbow-shaped 
image in a way that (roughly) maintains the scale in the original 
image.

USAGE NOTES:
Although the new image keeps the same scale as the original, the
created image will have a larger number of pixels (because of all
the empty pixels).

The attempt at non-distortion applies only to the central horizontal
band of the image. Depending on the initial aspect ratio, you will
see distortion above and below that centerline.  (The larger the
initial aspect ratio, the smaller the distortion will be.)

BUGS: 

If the aspect ratio isn't wide enough, then aspect ratio cannot
be preserved.  (This isn't actually a bug, it's basic geometry.)
In particular, you want width/height > angle / 114.6.
For instance, for default 180-degree bow, width/height > 1.57
The program will still "work" in this case, but scale and aspect
ratio will be compromised.

Because it uses plug-in-polar-coords, it has, as an intermediate
step, to resize the image, in some cases by quite a large factor.
(And pan images tend to be pretty large to begin with.)  So there
could be problems on computers with limited memory.  It might
have made more sense to just enhance the plug-in directly.

Disabled use of angle<45, since that leads to huge intermediate
images!

Currently, this tries to maintain scale along the middle of the 
imageone can imagine situations when it would be preferable to
keep the scale accurate at the top or the bottom of the image.
'''

from gimpfu import *
import process

def pan_to_bow(img,angle,arc_up):
    with process.UndoContext(img):
        process.pan_to_bow(img,angle,arc_up)

process.pfreg(pan_to_bow,
              [
                  (PF_IMAGE, "img", "Input image", None),
                  (PF_SLIDER, "angle", "Angle of circle", 180, (45,360,15)),
                  (PF_OPTION, "arc_up", "Arc direction", 0,
                   ("Rainbow", "Smile")),
              ],
              name="Pan to Bow",
              description=DESCRIPTION,
              author="theilr",
              year="2022",
              menu="<Image>/Filters/theilr"
)

main()
