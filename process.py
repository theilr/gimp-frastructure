'''Image processing modules'''


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License Version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at http://www.gnu.org/licenses for
# more details.

from __future__ import print_function, division
import math
from gimpfu import *

############################
## General utility functions

def flip_orient(layer,orientation):
    '''shorter name for pdb.gimp_item_transform_flip_simple'''
    return pdb.gimp_item_transform_flip_simple(layer,
                                               orientation,
                                               True,0)
def flip_v(layer):
    return flip_orient(layer,ORIENTATION_VERTICAL)
def flip_h(layer):
    return flip_orient(layer,ORIENTATION_HORIZONTAL)
def flip(layer,hflip=False,vflip=False):
    if hflip:
        layer = flip_h(layer)
    if vflip:
        layer = flip_v(layer)
    return layer

def visible_base(img,hflip=False,vflip=False,name="VisibleBase"):
    '''copy visible to layer, then flip horizontally and/or vertically'''
    ## copy visble to layer
    layer = pdb.gimp_layer_new_from_visible(img,img,name)
    img.add_layer(layer,-1)
    ## and flip if needed
    layer = flip(layer,hflip,vflip)
    return layer

def layer_fill_color(layer,color,respect_selection=False):
    '''
    fill a layer with a solid color,
    optionally respecting the selection, if there is one
    '''
    fg_orig = gimp.get_foreground()
    gimp.set_foreground(color)
    if respect_selection:
        pdb.gimp_edit_fill(layer,FILL_FOREGROUND)
    else:
        layer.fill(FILL_FOREGROUND)
    gimp.set_foreground(fg_orig)

def merge_down_active_layer(img):
    '''
    to keep layers from piling up, merge down from the current layer,
    return the layer that, after the merge, is then current
    '''
    img.merge_down(img.active_layer,0)
    return img.active_layer

#############################
## Image processing functions

def wide_blur(img, layer, radius):
    '''apply gauss-filter in place to layer'''
    ## multiple applications of gauss-filter if radius > 500

    # How many times
    nruns = int(math.ceil((radius/500)**2))
    if nruns > 1:
        radius = int(math.sqrt(radius*radius/nruns))
    for _ in range(nruns):
        pdb.plug_in_gauss(img,layer,radius, radius, 0)

def cheap_hdr(img,layer,r_blur,f_opacity):
    '''reduce global contrast without affecting local contrast'''
    ## then later on when you stretch contrast globally,
    ## you effectively enhance local contrast
    ov_layer = visible_base(img,name="Cheap HDR")
    wide_blur(img,ov_layer,r_blur)
    pdb.gimp_drawable_desaturate(ov_layer,3)
    pdb.gimp_invert(ov_layer)
    ov_layer.mode = LAYER_MODE_OVERLAY
    ov_layer.opacity = f_opacity

def sharpen(img,layer,r_sharp,s_l_mode):
    '''makes a new layer that is unsharp-mask of visible image'''
    sh_layer = visible_base(img,name="Sharpened")
    pdb.plug_in_unsharp_mask(img,sh_layer,r_sharp,0.5,0)
    sh_layer.mode = s_l_mode

def stretch(img,layer,f_stretch):
    '''makes a new layer that stretches contrast of visible image'''
    st_layer = visible_base(img,name="Stretched")
    pdb.gimp_drawable_levels_stretch(st_layer)
    #pdb.plug_in_c_astretch(img,st_layer)
    st_layer.opacity = f_stretch

def vignette(img,layer,lighten_corners,blur_radius,opacity,noise_spread):

    ## make a new layer
    vig_layer = img.new_layer("Vignette",img.width,img.height,
                              opacity=opacity,mode=LAYER_MODE_OVERLAY)
    ## paint it white (or black)
    pdb.gimp_drawable_fill(vig_layer,WHITE_FILL)
    if not lighten_corners:
        pdb.gimp_invert(vig_layer)

    ## select an ellipse
    pdb.gimp_image_select_ellipse(img,CHANNEL_OP_REPLACE,
                                  0,0,img.width,img.height)

    ## paint the ellipse gray
    layer_fill_color(vig_layer,(0.5,0.5,0.5),
                     respect_selection=True)

    ## un-select the ellipse selection
    pdb.gimp_selection_none(img)

    ## blur the gray ellipse into the light or dark corners
    wide_blur(img,vig_layer,blur_radius)

    ## maybe spread noise
    if noise_spread:
        ## why spread it more than 50 pixels?
        pdb.plug_in_spread(img,vig_layer,min([50,blur_radius]),min([50,blur_radius]))

###############################
## Image manipulation functions

def multiply_size_by_orientation(item,n,m,orientation):
    if orientation == ORIENTATION_VERTICAL:
        n,m = m,n
    w = n * item.width
    h = m * item.height
    return w,h

def reflect(img,orientation):
    '''abut visible with its mirror image'''
    w,h = multiply_size_by_orientation(img,2,1,orientation)
    img.resize(w,h,0,0)
    nextlayer = visible_base(img,name="Mirror")
    nextlayer = flip_orient(nextlayer,orientation)
    pdb.gimp_image_merge_down(img,nextlayer,0)

def mirror(img, layer, m_horiz, m_vert, ul_hflip, ul_vflip):
    '''abut visible with reflections: horizontal or vertical or both'''

    ## Mirror is like 'accordion' but only single reflections allowed

    ## first copy visble to layer and flip if needed
    layer = visible_base(img,hflip=ul_hflip,vflip=ul_vflip,name="Mirror")

    ## now mirror the base, horizontally and/or vertically
    if m_horiz:
        reflect(img,0)
    if m_vert:
        reflect(img,1)

def accord_1d(img,layer,n,do_flip,orientation):
    '''helper function for accordion -- just does 1d'''
    ## make the image big enough
    h,v = multiply_size_by_orientation(layer,n,1,orientation)
    img.resize(h,v,0,0)
    for i in range(n):
        nextlayer = layer.copy()
        img.add_layer(nextlayer,-1)
        if do_flip and i % 2: ## flip the odd tiles
            nextlayer = flip_orient(nextlayer,orientation)
        x,y = multiply_size_by_orientation(layer,i,0,orientation)
        nextlayer.set_offsets(x,y)
        if i > 0:
            pdb.gimp_image_merge_down(img,nextlayer,0)

    layer = merge_down_active_layer(img)
    return layer

def accordion(img, layer, n_horiz, n_vert, do_flip, ul_hflip, ul_vflip):
    '''reflect the image horizontally and/or vertically multiple times'''
    ## first copy visble to base layer and flip if needed
    layer = visible_base(img,hflip=ul_hflip,vflip=ul_vflip,name="Accordion")

    if n_horiz > 1:
        layer = accord_1d(img,layer,n_horiz,do_flip,ORIENTATION_HORIZONTAL)
    if n_vert > 1:
        layer = accord_1d(img,layer,n_vert,do_flip,ORIENTATION_VERTICAL)

def scale_to_square(img):
    '''
    rescale/distort img so that it is a square of equal area to the original
    '''
    h = img.width
    v = img.height
    hv = int(math.sqrt(h*v))
    pdb.gimp_image_scale(img,hv,hv)

def scale_to_fibonacci(img,squareflag):
    '''
    rescale img so that its pixel counts in horiz and vertical dimension are
    successive (or if img is square, equal) Fibonacci numbers.
    if squareflag is set, then make img square first, so scaled is also square
    '''
    if squareflag:
        scale_to_square(img)
    w = img.width
    h = img.height
    a = b = 1
    while b < max([w,h]):
        b,a = a+b,b
    if b > max([w,h]):
        b,a = a,b-a
    if h > w:
        b,a = a,b
    if h == w:
        b,a = b,b
    img.scale(b,a)

def rotate_simple(img,layer,quarterturns):
    '''rotate the layer 90 degrees X number of quarter turns'''
    quarterturns = quarterturns % 4 # so 0 <= q < 4
    if quarterturns:
        pdb.plug_in_rotate(img,layer,quarterturns,False)

def fibonacci_prev(n):
    g = (math.sqrt(5)+1)/2
    print('prev:',n,g)
    return round(n/g)

def fibonacci_next(n):
    g = (math.sqrt(5)+1)/2
    return round(n*g)

def fibonacci_spiral(img,aspect,q_turn,blend,opacity,merge_down):
    '''
    Third attempt at a fibonacci spiral, with new options,
    and ability to work with landscape, portrait, or square images
    img:  image
    aspect: 1 for square, 0 for rectangle
    q_turn: number of quarter-turns per new layer
    blend:  LAYER_MODE for overlapping layers (only in rectangle mode)
    opacity: opacity for overlapping layers (only in rectangle mode)
    merge_down: if True, then flatten all the layers at the end
    '''
    portrait_flag = sq_flag = False
    if aspect == 1 or img.height == img.width:
        sq_flag = True
        blend = LAYER_MODE_NORMAL
        opacity = 100.
    if img.height > img.width:
        portrait_mode = True
        pdb.gimp_image_rotate(img,ROTATE_90)

    if img.height > img.width:
        raise RuntimeError("Failed to rotate portrait mode")

    ## For rectangular aspect, only rotate 90 or 270
    if aspect != 1 and q_turn in [0,2]:
        print("Must rotate CW or CCW; changing to CW")
        q_turn = 1

    scale_to_fibonacci(img,sq_flag)
    baselayer = visible_base(img,name="Base") ## copy a new layer
    nxtsize = min([img.width,img.height])
    cursize = fibonacci_next(nxtsize)
    count = 0
    x = y = 0
    while cursize > nxtsize:
        count += 1
        cursize,nxtsize = nxtsize,cursize-nxtsize
        nxtlayer = baselayer.copy()
        img.add_layer(nxtlayer,-1)
        new_width = nxtsize if sq_flag else cursize
        nxtlayer.scale(new_width,nxtsize,False)
        rotate_simple(img,nxtlayer,count*q_turn)
        ## Complicated logic to get x,y coordinates of
        ## UL corner of count'th layer in Fibonacci spiral
        if count % 4 == 1:
            x += cursize
        if count % 4 == 2:
            y += cursize
        if sq_flag:
            if count % 4 == 2:
                x += cursize-nxtsize
            if count % 4 == 3:
                x -= nxtsize
                y += cursize-nxtsize
            if count % 4 == 0:
                y -= nxtsize
        nxtlayer.set_offsets(x,y)
        nxtlayer.mode = blend
        nxtlayer.opacity = opacity
    img.resize_to_layers()
    if merge_down:
        img.flatten()
    if portrait_mode:
        ## undo rotation to get image back into portrait aspect
        pdb.gimp_image_rotate(img,ROTATE_270)

def fuzzy_select(img,layer,threshold,xlist,ylist):
    ## set threshold
    thresh_orig = pdb.gimp_context_get_sample_threshold_int()
    pdb.gimp_context_set_sample_threshold_int(threshold)
    ## obtain selection from first point in list(s)
    pdb.gimp_image_select_contiguous_color(img,CHANNEL_OP_REPLACE,layer,
                                           xlist[0],ylist[0])
    ## add selection from subsequent points in list(s)
    for x,y in zip(xlist[1:],ylist[1:]):
        pdb.gimp_image_select_contiguous_color(img,CHANNEL_OP_ADD,layer,x,y)
    ## retst threshold back to original
    pdb.gimp_context_set_sample_threshold_int(thresh_orig)

def jagged_border(img,layer,border_shape,border_white,border_size,
                  thresh,fill_islands,one_pixel_border):
    if border_shape == 0:
        ## For rectangular border, to avoid rounded corners,
        ## run twice: once vertical-only and once horizontal-only
        jagged_border_run(img,layer,1,border_white,border_size,
                          thresh,fill_islands,one_pixel_border)
        jagged_border_run(img,layer,2,border_white,border_size,
                          thresh,fill_islands,one_pixel_border)
    else:
        ## If not Rectangular, than just run once
        jagged_border_run(img,layer,border_shape,border_white,border_size,
                          thresh,fill_islands,one_pixel_border)

def jagged_border_run(img,layer,border_shape,border_white,border_size,
                  thresh,fill_islands,one_pixel_border):
    ## add two new layers
    tmp_layer = visible_base(img,name="tmp")
    cpy_layer = visible_base(img,name="border")

    ## black layer
    pdb.gimp_edit_fill(tmp_layer,WHITE_FILL)
    pdb.gimp_drawable_invert(tmp_layer,True)

    xlo=ylo=0
    xhi=img.width
    yhi=img.height
    fcn_select = pdb.gimp_image_select_rectangle

    if border_shape == 1: ## horizontal only
        ylo += border_size
        yhi -= border_size
    elif border_shape == 2:## vertical only
        xlo += border_size
        xhi -= border_size
    else: ## horizontal and vertical (ie, rectangle or ellipse)
        xlo += border_size
        xhi -= border_size
        ylo += border_size
        yhi -= border_size
    if border_shape == 3: ## ellipse, not rectangle
        fcn_select = pdb.gimp_image_select_ellipse

    fcn_select(img,CHANNEL_OP_REPLACE,xlo,ylo,xhi-xlo,yhi-ylo)
    pdb.gimp_selection_invert(img)
    pdb.gimp_edit_fill(tmp_layer,WHITE_FILL)
    pdb.gimp_selection_none(img)
    wide_blur(img,tmp_layer,2*border_size)

    pdb.gimp_drawable_desaturate(cpy_layer,DESATURATE_LIGHTNESS)
    if not border_white:
        pdb.gimp_invert(cpy_layer)
    if one_pixel_border:
        pdb.gimp_image_select_rectangle(img,CHANNEL_OP_REPLACE,
                                        0,0,img.width,img.height)
        pdb.gimp_selection_shrink(img,1)
        pdb.gimp_selection_invert(img)
        pdb.gimp_edit_fill(cpy_layer,WHITE_FILL)
        pdb.gimp_selection_none(img)

    ## Note: ADDITION_MODE = LAYER_MODE_ADDITION_LEGACY != LAYER_MODE_ADDITION
    ## Here, legacy appears to work better
    ## Later, the mode applies to binary black and white masks, so doesn't matter
    cpy_layer.mode = ADDITION_MODE
    tmp_layer = merge_down_active_layer(img)

    fuzzy_select(img,tmp_layer,thresh,[0,img.width-1],[0,img.height-1])

    img.remove_layer(tmp_layer)
    bdr_layer = img.new_layer("Border",img.width,img.height)
    pdb.gimp_drawable_fill(bdr_layer, WHITE_FILL) ## ignores selection
    pdb.gimp_selection_invert(img) ## inverted selection is the interior
    pdb.gimp_invert(bdr_layer)     ## make interior black, border white
    pdb.gimp_selection_none(img)
    bdr_layer.mode = LAYER_MODE_ADDITION

    if fill_islands:
        ## select from deep interior, inverse of that is new jagged border
        fuzzy_select(img,bdr_layer,thresh,[img.width//2],[img.height//2])
        pdb.gimp_selection_invert(img)
        pdb.gimp_edit_fill(bdr_layer,WHITE_FILL) ## respects selection
        pdb.gimp_selection_none(img)

    if not border_white:
        pdb.gimp_invert(bdr_layer)
        bdr_layer.mode = LAYER_MODE_MULTIPLY

def pan_to_bow(img,angle_degrees,arc_up=True):
    ## Using a new layer from visible, we obtain transparent background

    ## since background is going to be transparent, make bottom layer invisible
    ## so it doesn't show through
    bottom_layer = img.active_layer
    layer = visible_base(img,vflip=bool(arc_up),name="PanToBow")
    if bottom_layer:
        bottom_layer.visible=False

    h_o = layer.height
    w_o = layer.width
    max_degrees = 360.*w_o/(h_o*math.pi)
    top_degrees = math.pi*max_degrees/2
    if angle_degrees > max_degrees:
        ## causes inner radius to be zero
        print('max angle:',max_degrees,'degrees')
    if angle_degrees > top_degrees:
        ## causes shrinkage to occur in outer radius < h_o
        print('top angle:',top_degrees,'degrees')
    angle_radians = angle_degrees * math.pi / 180.
    bow_radius = int( w_o / angle_radians )
    radius_inner = max([0, bow_radius - h_o//2])
    radius_outer = radius_inner + h_o
    #print('radii:',radius_inner,radius_outer)
    pad_sides = int( w_o * (360/angle_degrees - 1)/2 )
    w_expanded = int( w_o + 2*pad_sides )
    h_expanded = int( h_o + radius_inner )

    #print('pad_sides:',pad_sides)

    img.resize(w_expanded,h_expanded,pad_sides,0)
    layer.resize(w_expanded,h_expanded,pad_sides,0)
    layer.scale(w_expanded,2*h_expanded,False)
    img.resize(w_expanded,2*h_expanded,0,0)

    #print('img befor:',img.width,img.height)
    pdb.plug_in_polar_coords(img,layer,100,180,False,False,True)
    #print('img after:',img.width,img.height)

    sinx = abs(math.sin(angle_radians/2))
    cosx = abs(math.cos(angle_radians/2))
    if angle_degrees < 180:
        w_crop = 2*radius_outer*sinx
        h_crop = radius_outer - radius_inner*cosx
    else:
        w_crop = 2*radius_outer
        h_crop = (1+cosx)*radius_outer

    w_crop = int(w_crop)
    h_crop = int(h_crop)

    #print('w:',2*radius_outer,w_expanded,w_crop,(w_expanded-w_crop)//2)
    #print('crop:',w_crop,h_crop)
    ## img and exp should be the same
    #print(' img:',img.width,img.height)
    #print(' exp:',w_expanded,2*h_expanded)
    if img.width < img.height:
        ## some shrinkage occurred
        f_shrink = img.width / (2*radius_outer)
        w_crop = int( f_shrink*w_crop )
        h_crop = int( f_shrink*h_crop )
        h_off = img.height//2 - int(f_shrink*radius_outer)

        img.crop(w_crop,h_crop,0,h_off)
    else:
        ## offset is in width
        img.crop(w_crop,h_crop,(img.width - w_crop)//2,0)

    if arc_up:
        layer = flip_v(layer)

    return layer

def infinity(img,bkg_color,pad_degrees=0,vfix=0):
    '''bend a high-aspect ratio image into a horizontal figure-eight'''
    pad = pad_degrees/(720-2*pad_degrees)
    if pad > 0:
        pixpad = int(pad*img.width)
        new_width = img.width + 2*pixpad
        img.resize(new_width,img.height,pixpad,0)

    ## make sure width evenly divisible by 4, cropping if necessary
    new_width = 4*(img.width//4)
    if new_width != img.width:
        img.crop(new_width,img.height,0,0)
    ## make main layer from visible image
    main_layer = visible_base(img,name="InfinityBase")
    h = main_layer.height
    w = main_layer.width
    aux_layers = []
    for k in range(4):
        ## Put 1/4 of the image into an aux image
        img_aux = gimp.Image(img.width,img.height,RGB)
        layer = pdb.gimp_layer_new_from_drawable(main_layer, img_aux)
        img_aux.add_layer(layer)
        img_aux.crop(w//4,h,k*w//4,0)
        ## Make a rainbow or smile
        rainbow = bool(k in [2,3])
        layer = pan_to_bow(img_aux,180,rainbow)
        ## orient as needed
        if k in [0,3]:
            layer = flip(layer,True,True)
        ## add rainbow layer back to original image
        layer_new = pdb.gimp_layer_new_from_drawable(layer, img)
        img.add_layer(layer_new)
        aux_layers.append(layer_new)

    W = aux_layers[0].width
    H = aux_layers[0].height
    img.resize(2*W-h,2*H,0,0)
    ## offsets at H-vfix,vfix instead of H,0 are used to
    ## squeeze out rounding-effect artifact of horizontal line
    hfix=1 ## not sure why this helps, but it seems to
    aux_layers[0].set_offsets(hfix,H-vfix)
    aux_layers[1].set_offsets(0,vfix)
    aux_layers[2].set_offsets(W-h,H-vfix)
    aux_layers[3].set_offsets(W-h+hfix,vfix)
    for _ in range(3):
        img.lower_layer(aux_layers[3])

    ## Make a solod-color background layer
    tmp_layer = gimp.Layer(img,"Infinity Background",img.width,img.height)
    img.add_layer(tmp_layer)
    layer_fill_color(tmp_layer,bkg_color)
    img.lower_layer(tmp_layer)

############################
## Define the 'undo' context

class UndoContext:
    '''code within this context has an Undo associated with it'''
    def __init__(self,img):
        self.img=img

    def __enter__(self):
        pdb.gimp_undo_push_group_start(self.img)
        return None

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print('exc:',exc_type,exc_value,exc_tb)
        pdb.gimp_undo_push_group_end(self.img)
        return True

##################################
## Wrapper for register() function

def pfreg(fcn,fcn_arglist,
          author="Anonymous",
          copyright=None,
          year=0,
          fcn_name=None,
          description=None,
          name=None,
          menuname=None,
          menu=None,
          imgtype="*"):
    '''
    pfreg = python-fu register;
    wrapper for register() function that is intended to be a little easier to use
    '''

    fcn_name = fcn_name or fcn.__name__
    pf_fcn_name = "python_fu_" + fcn_name

    name = name or fcn_name
    menuname = menuname or name+"..."
    description = description or name
    copyright = copyright or "(c) "+author
    menu = menu or "<Image>/Filters"
    #menupath = menu + "/" + menuname

    register(pf_fcn_name,
             name,
             description,
             author,
             copyright,
             str(year),
             menuname,
             imgtype,
             fcn_arglist,
             [],
             fcn,menu=menu)
