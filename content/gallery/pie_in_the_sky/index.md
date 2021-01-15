+++
# Beginning of HEADER
# This is a Markdown file!
title = "A pie in the sky"

# Tags: can be used for filtering images/plots.
tags = ["galaxy", "simulations", "cosmology", "python"]

# to allow Latex symbols
math = true

# Featured image
# To use, add an image named `featured.jpg/png` to your project's folder. 
[image]
  # Caption (optional) DO NOT USE THIS CAPTION OPTION
  caption = ""
  
  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = "Smart"

# End of HEADER
# The following parameters are optional. Remember to leave two blank spaces at the end of each section (this introduces a new line in Markdown)
+++

Caption: On large scales, the Universe resembles a giant web. But the appearance of this cosmic web is very different when seen through different observables. The movie shows some of these looks using a slice through the output from a numerical simulation. The quantities shown are, from the top slice in clockwise order: the matter (over)density, hydrogen neutral fraction, gas temperature, metallicity (= mass fraction of elements heavier than helium), and stellar mass (relative to the Sun mass).

Author: Enrico Garaldi

Affiliation: University of Bonn

Original Image: [link](http://droettboom.com/jhepc2018-judge-packet/entry19.html)

```python
# The data required to run this code can be found at https://drive.google.com/file/d/1jRb8SweYSydJYufjARoE4VCH0wm1FoQE/view

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from math import pi as PI
from scipy.ndimage.interpolation import map_coordinates
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import register_cmap

__license__   = "GNU GPLv3 <https://www.gnu.org/licenses/gpl.txt>"
__copyright__ = "20221 Enrico Garaldi"
__author__    = "Enrico Garaldi <egaraldi@uni-bonn.de>"
__version__   = "1.0"


# create & register a new colormap
_cm_name = 'BlackToYellow'
_cm_data = { 'red'   : ((0.0, 0.0, 0.0), 
                        (0.25, 0.0, 0.0),
                        (1.0, 1.0, 1.0)),
             'green' : ((0.0, 0.0, 0.0), 
                        (0.25, 0.0, 0.0),
                        (1.0, 1.0, 1.0)),
             'blue'  : ((0.0, 0.0, 0.0),
                        (0.25, 0.0, 0.0),
                        (1.0, 0.0, 0.0))
           }
register_cmap(name=_cm_name, cmap=LinearSegmentedColormap(_cm_name,_cm_data))


# create a function to create a pie plot
def PiePlot(ax, *args, radius=0.8, initial_angle=0.0, cmaps=None, vmins=None, vmaxs=None, edge_deltaR=0, bcm_Rmin=0.85, 
        bcm_Rmax=0.90, bcm_Rticklabels=0.95, bcm_Rlabel=1.0, bcm_Nsteps=100, bcm_ticks=5, bcm_ticklabels=None, 
        bcm_buffer_angle_frac=0.1, bcm_labels=None, bcm_labels_fontsize=15, bcm_ticklabels_fontsize=10, bcm_labels_tilt=None, 
        bcm_ticklabels_tilt=None, bcm_edge_deltaR=0, resample=None):
    """
    Plots a (collection of) field(s) in a circle with slices showing different
    fields. It also produces circular colorbars.

    Params:
    ------
    ax                      : matplotlib.Axes
                              Axes to draw on
    *args                   : (set of) squared 2D np.array
                              fields that will be drawn in each slice (one per slice).
                              The number of fields determines the number of slices.

    radius                  : float in (0,1]
                              radius of circular plot in unit of half field side
    initial_angle           : float
                              offset from 0 of the first slice in radians
    cmaps                   : list of string
                              For each field, name of the matplotlib colormap to use. 
                              If None, a set of default colormaps is used.
    vmins                   : list of floats
                              For each field, vmin to use in the colormap.
                              If None, vmin = min(field)
    vmaxs                   : list of floats
                              For each field, vmax to use in the colormap.
                              If None, vmax = max(field)
    edge_deltaR             : float in [0,1)
                              thickness of plot edge (fraction of the radius)
    bcm_Rmin                : float > 0
                              inner radius of the colorbar
    bcm_Rmax                : float > 0,1
                              outer radius of the colorbar
    bcm_Rticklabels         : float > 0
                              radius of colorbar ticklabels
    bcm_Rlabel              : float > 0
                              radius of colorbar label
    bcm_Nsteps              : int
                              number of steps used to build the colorbar
    bcm_ticks               : int OR list of ints OR list of list of floats
                              if int, number of ticks in the colorbar,
                              if list of int, number of ticks for each field
                              if list of list of floats, tick values for each field
    bcm_ticklabels          : list of list of strings
                              ticklabels for each fields.
                              If None, the numerical value is printed using the format '%.2g'
    bcm_buffer_angle_frac   : float in [0,0.5)
                              angular buffer between slice edge and colorbar in units
                              of the slice angle
    bcm_labels              : list of string
                              colorbar labels for each field
    bcm_labels_fontsize     : int
                              font size for colormap label
    bcm_ticklabels_fontsize : int
                              font size for colormap ticklabels
    bcm_labels_tilt         : float OR list of floats
                              if float, impose a fixed tilt for the labels (in degrees)
                              if list of floats, impose a fixed tilt for each field
                              if None, the labels are tangential to the colorbar
    bcm_ticklabels_tilt     : float OR list of floats
                              if float, impose a fixed tilt for the ticklabels (in degrees)
                              if list of floats, impose a fixed tilt for each field
                              if None, the ticklabels are tangential to the colorbar
    bcm_edge_deltaR         : float in [0,1)
                              thickness of colorbar edge (fraction of the radius)
    resample                : float
                              resample the input field by the factor provided (i.e. if the input fields 
                              have shape [Nx,Ny], they will be resampled to [resample*Nx,resample*Ny]
                              if None, no resample will be performed
    """

    fields  = list(args)  #enable modifications to args
    Nfields = len(args)

    #check input
    for field in fields:
        if field.ndim != 2:
            print("ERROR: fields must be 2-dimensional!")
            return
        nx,ny = field.shape
        if nx != ny:
            print("ERROR: fields must be squared!")
            return

    if (radius > 1) | (radius <= 0):
        print("ERROR: radius must be in (0,1]!")
        return

    if (cmaps is None):
        cmaps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))[0:Nfields]
        

    if (vmins is None):
        vmins = []
        for field in fields:
            vmins.append( field.min() )

    if (vmaxs is None):
        vmaxs = []
        for field in fields:
            vmaxs.append( field.max() )
    
    if (bcm_Rmin <= 0):
        print("ERROR: bcm_Rmin must be > 0!")
        return

    if (bcm_Rmax <= 0):
        print("ERROR: bcm_Rmax must be > 0!")
        return

    if (bcm_Rticklabels <= 0):
        print("ERROR: bcm_Rticklabels must be > 0!")
        return

    if (bcm_Rlabel <= 0):
        print("ERROR: bcm_Rlabel must be > 0!")
        return

    if (bcm_buffer_angle_frac >= 0.5) | (bcm_buffer_angle_frac < 0):
        print("ERROR: bcm_buffer_angle_frac must be in [0,0.5)!")
        return

    if (bcm_edge_deltaR >= 1) | (bcm_edge_deltaR < 0):
        print("ERROR: bcm_edge_deltaR must be in [0,1)!")
        return

    if (bcm_buffer_angle_frac >= 0.5) | (bcm_buffer_angle_frac < 0):
        print("ERROR: bcm_buffer_angle_frac must be in [0,0.5)!")
        return

    if (bcm_edge_deltaR >= 1) | (bcm_edge_deltaR < 0):
        print("ERROR: bcm_edge_deltaR must be in [0,1)!")
        return

    if (bcm_labels is None):
        bcm_labels = []
        for i in range(Nfields):
            bcm_labels.append( "field %i"%i )

    bcm_ticks_in_input = False
    if isinstance(bcm_ticks, int):
        bcm_Nticks = [bcm_ticks]*Nfields
    elif isinstance(bcm_ticks, list):
        if isinstance(bcm_ticks[0], int):
            bcm_Nticks = bcm_ticks
        elif isinstance(bcm_ticks[0], list):
            bcm_Nticks = [len(_Nticks) for _Nticks in bcm_ticks]
            bcm_ticks_in_input = True
        else:            
            print("ERROR: bcm_ticks can only be a int OR a list of int OR a list of list of int!")
            return
    if (bcm_labels_tilt is not None):
        if not isinstance(bcm_labels_tilt, list):
            bcm_labels_tilt = [bcm_labels_tilt]*Nfields

    if (bcm_ticklabels_tilt is not None):
        if not isinstance(bcm_ticklabels_tilt, list):
            bcm_ticklabels_tilt = [bcm_ticklabels_tilt]*Nfields

    if (resample is not None) and (resample != 1):
        px = ( np.arange(resample*nx) + 0.5 ) / resample 
        py = ( np.arange(resample*ny) + 0.5 ) / resample 
        newcoords = np.meshgrid(px,py)
        for i in range(len(fields)):
            fields[i] = map_coordinates(fields[i], newcoords, order=1, mode='nearest').T
        nx,ny = fields[0].shape


    slice_angle = 2*PI/Nfields
    Lside = nx
    xc = nx//2
    yc = ny//2

    xs,ys = np.mgrid[0:nx, 0:ny]
    pixel_angle = np.arctan2(ys-yc, xs-xc) + PI  #[0, 2*PI]
    pixel_angle = (pixel_angle - initial_angle)%(2*PI)
    pixel_radius = np.sqrt( (xs-xc)**2 + (ys-yc)**2 )
    

    #plot edge
    edgepixels = np.ma.masked_where( (pixel_radius >= (radius+bcm_edge_deltaR)*Lside//2),
                                     np.ones_like(pixel_angle) )
    ax.imshow(edgepixels, cmap='Greys_r', vmin=0, vmax=0)

    for i,field in enumerate(fields):
        #plot field
        masked_field = np.ma.masked_where( (pixel_angle  <      i*slice_angle) | 
                                           (pixel_angle  >  (i+1)*slice_angle) |  #there should be a >= here, but this sometimes produce empty pixels, so I removed it
                                           (pixel_radius >  radius*Lside//2)    , field )
        ax.imshow(masked_field, cmap=cmaps[i], vmin=vmins[i], vmax=vmaxs[i])

        #bcm = bent colormap
        th_min =       i*slice_angle + bcm_buffer_angle_frac*slice_angle
        th_max =   (i+1)*slice_angle - bcm_buffer_angle_frac*slice_angle
        th_mid = (i+0.5)*slice_angle

        #colormap edge
        bcm_edge_deltatheta = np.arcsin(bcm_edge_deltaR/bcm_Rmax)
        edgepixels = np.ones_like(pixel_angle)
    
        edgepixels = np.ma.masked_where( (pixel_radius <  (bcm_Rmin-bcm_edge_deltaR)*Lside//2) | 
                                         (pixel_radius >= (bcm_Rmax+bcm_edge_deltaR)*Lside//2) |
                                         (pixel_angle  <   th_min-bcm_edge_deltatheta)         |
                                         (pixel_angle  >=  th_max+bcm_edge_deltatheta)         ,
                                         np.ones_like(pixel_angle) )

        ax.imshow(edgepixels, cmap='Greys_r', vmin=0, vmax=0)


        #colormap
        vmin = vmins[i]
        vmax = vmaxs[i]
        pixels = 10*np.ones_like(pixel_angle)
        for j in range(bcm_Nsteps):
            step_min =     j/bcm_Nsteps
            step_max = (j+1)/bcm_Nsteps
            step_mid = j/(bcm_Nsteps-1)
            w = (pixel_radius >= bcm_Rmin*Lside//2) & (pixel_radius < bcm_Rmax*Lside//2) & (pixel_angle >= th_min+step_min*(th_max-th_min)) &\
                (pixel_angle < th_min+step_max*(th_max-th_min))
            pixels[w] = step_mid
        cm = np.ma.masked_greater(pixels, 1)
        ax.imshow(cm, cmap=cmaps[i])


        for j in range(bcm_Nticks[i]):
            if bcm_ticks_in_input:
                jtick = (bcm_ticks[i][j] - vmin) / (vmax - vmin)
            else:
                jtick = j/(bcm_Nticks[i]-1)
            xtick = xc - bcm_Rticklabels*Lside//2*np.sin(th_min+jtick*(th_max-th_min)+initial_angle)
            ytick = yc - bcm_Rticklabels*Lside//2*np.cos(th_min+jtick*(th_max-th_min)+initial_angle)
            if (bcm_ticklabels_tilt is None):
                tilt  = ( (th_min + jtick*(th_max-th_min) + initial_angle)*180/PI )%360
                if (verticalalignment > 90) and (tilt <= 270): tilt += 180
            else:
                tilt = bcm_ticklabels_tilt[i]
            if (bcm_ticklabels is None):
                vtick = "%.2g"%(vmin + jtick*(vmax-vmin))
            else:
                vtick = bcm_ticklabels[i][j]
            ax.text(xtick, ytick, vtick, verticalalignment='center', horizontalalignment='center', rotation=tilt, transform=ax.transData, fontsize=bcm_ticklabels_fontsize)
        xlabel = xc - bcm_Rlabel*Lside//2*np.sin(th_min+0.5*(th_max-th_min)+initial_angle)
        ylabel = yc - bcm_Rlabel*Lside//2*np.cos(th_min+0.5*(th_max-th_min)+initial_angle)
        if (bcm_labels_tilt is None):
            tilt   = ( (th_mid+initial_angle)*180/PI )%360
            if (tilt > 90) and (tilt <= 270): tilt += 180
        else:
            tilt = bcm_labels_tilt[i]
        ax.text(xlabel, ylabel, bcm_labels[i], verticalalignment='center', horizontalalignment='center', rotation=tilt, transform=ax.transData, fontsize=bcm_labels_fontsize)



#load simulation
print("Loading simulation data...")
fields = np.load('fields_resampled.npz')
gal_field = np.load('gal_field2.npy')

print(" Plotting...")
fig = plt.figure(figsize=(10,10))
gs = GridSpec(1,1)
ax_img = fig.add_subplot( gs[0  ,0] )

for i,theta_in in enumerate(np.arange(360,0,-0.5)):
    PiePlot(ax_img, 
               np.log10(fields['met']), fields['temp'] /1e3, np.log10(fields['xHI' ]), np.log10(fields['oden']), np.log10(gal_field), 
               initial_angle=theta_in/180*PI,
               cmaps=['terrain', 'YlOrRd', 'Spectral', 'viridis', 'BlackToYellow'], 
               vmins=[-23, 7.7, -5.1, -1.1, 0], 
               vmaxs=[0, 20.1, -3.9, 2.1, 7],
               radius=0.815,
               edge_deltaR=0.005,
               bcm_Nsteps=100, 
               bcm_Rmin=0.83, 
               bcm_Rmax=0.88, 
               bcm_ticks=[[-20,-15,-10,-5], [8,12,16,20],[-5,-4.5,-4], [-1,0,1,2], [2,4,6]], 
               bcm_buffer_angle_frac=0.015,
               bcm_Rticklabels=0.94, 
               bcm_Rlabel=1.05,
               bcm_labels=[r'$\log(Z/Z_{\odot})$', r'$T \, [10^3 \, {\rm K}]$', r'$\log(x_{\rm HI})$', r'$\log(1+\delta_{\rm b})$', r'$\log(M_*/M_\odot)$'],
               bcm_labels_fontsize=20, 
               bcm_ticklabels_fontsize=17, 
               bcm_labels_tilt=None, 
               bcm_ticklabels_tilt=0,
               bcm_edge_deltaR=0.005,
               resample=None)

    print(" Saving final output (%i)..."%i)
    ax_img.set_axis_off()
    fig.savefig('pie5_%i.png'%i, pad_inches=-1, dpi=300)
    ax_img.clear()
plt.close(fig)
```

_Press the tag below to see more examples_
