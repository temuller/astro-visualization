+++
# Beginning of HEADER
# This is a Markdown file!
title = "Artistic galaxy tracks"

# Tags: can be used for filtering images/plots.
tags = ["galaxy", "simulations", "python"]

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

Caption: The dominant matter component of the Universe is a mysterious substance dubbed Dark Matter, which drives the formation of galaxies and cosmic structure thanks to its gravitational attraction, but does not interact with light. Every galaxy is embedded in a clump of Dark Matter called halo, approximately ten times larger than the galaxy itself. Some of these haloes were already in place billions of years ago, and since then did not increased their mass significantly. For these reasons, they are called 'old'. Others, despite having the same mass today, are still actively growing (i.e. accreting new material). Hence, such haloes are dubbed 'young'. Haloes in the Universe - and hence the galaxies they host - are organized in the so-called cosmic web, an ubiquitous network of long filament, intersecting in dense knots, embedded in vast empty regions that make up most of the volume. Filaments and knots host gaseous material as well, providing a prime way for matter to move across the Universe. More than ten years ago, it was realised that Dark Matter haloes of different age (but same mass) show very different clustering properties. Old ones are found much closer to each other than young haloes. The reason has become clearer in 2017, when it was shown that this effect is driven by the halo location in the cosmic web. Such cosmic environment changes the fate of haloes that are otherwise similar. Young haloes reside in knots of the cosmic web, where they dominate the local gravitational potential and, thanks to the constant flow of material from the nearby filaments, can accrete material for their entire life, until today. On the other hand, old haloes live in the filaments themselves, where the supply of material is suppressed by the competing gravitational attraction of other haloes in the filament, and therefore their growth is easily stopped early on. The plot shows the effect of cosmic environment on the gas (top panels) and stars (bottom panels) of haloes of the same mass. Each column shows a different simulated galaxy. The two on the left are hosted by old haloes (and therefore live in filaments of the cosmic web), while the two galaxies on the right reside in young haloes (located in knots of the cosmic web). All panels are centered on the galaxy position. In old haloes, the gas first falls vertically onto a squashed structure (the filament), and then - from there - moves toward the halo itself. This is characteristic of accretion from filaments, as the latter is dominating the gravitational potential. For young haloes, however, gas falls in from multiple directions, corresponding to the many filaments converging into the knot where the halo reside. Stars show a simiar pattern, but the trajectory are more clustered, as stars are only contained in smaller galaxies that merge with the halo. Some of these can be clearly seen as thick tracks.

Author: Enrico Garaldi

Affiliation: University of Bonn

Original Image: [link](https://enricogaraldi.wixsite.com/egaraldi/outreach)

```python
# This script requires additional data file to run. Contact me if you are interested in having access to those

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 10000
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmaps
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patheffects as PathEffects


Ncolors=10
linewidth=1
alpha=0.1

Ntracks_to_plot = 2000  #-1 to use all

fig = plt.figure(figsize=(30,15))
fig.patch.set_facecolor('grey')
gs = GridSpec(515, 1017)
gs.update(left=0.0, right=1.0, bottom=0.0, top=1.0, wspace=0.0, hspace=0.1)
axTLL = fig.add_subplot(gs[  5: 255,   5: 255], projection='3d')
axTLC = fig.add_subplot(gs[  5: 255, 256: 506], projection='3d')
axTRC = fig.add_subplot(gs[  5: 255, 511: 761], projection='3d')
axTRR = fig.add_subplot(gs[  5: 255, 762:1012], projection='3d')
axBLL = fig.add_subplot(gs[260: 510,   5: 255], projection='3d')
axBLC = fig.add_subplot(gs[260: 510, 256: 506], projection='3d')
axBRC = fig.add_subplot(gs[260: 510, 511: 761], projection='3d')
axBRR = fig.add_subplot(gs[260: 510, 762:1012], projection='3d')


for i in range(8):
    if i==0:
        pos = np.load("tracks_gas_model1202.npy")
        ax = axTLL
    elif i==1:
        pos = np.load("tracks_gas_model2111.npy")
        ax = axTLC
    elif i==2:
        pos = np.load("tracks_gas_model1236.npy")
        ax = axTRC
    elif i==3:
        pos = np.load("tracks_gas_model1249.npy")
        ax = axTRR
    elif i==4:
        pos = np.load("tracks_stars_model1202.npy")
        ax = axBLL
    elif i==5:
        pos = np.load("tracks_stars_model2111.npy")
        ax = axBLC
    elif i==6:
        pos = np.load("tracks_stars_model1236.npy")
        ax = axBRC
    elif i==7:
        pos = np.load("tracks_stars_model1249.npy")
        ax = axBRR

    if i<4:
        cmap_name = 'ocean'
        color = cmaps.get_cmap(cmap_name)( np.linspace(0.0, 1.0, Ncolors, endpoint=True) )
    else:
        cmap_name = 'gnuplot'
        color = cmaps.get_cmap(cmap_name)( np.linspace(0.0, 1.0, Ncolors, endpoint=True) )
    
    
    
    Nsnaps, Ntracks, _ = pos.shape

    if((Ntracks_to_plot > 0) and (Ntracks_to_plot < Ntracks)):
        idxt = np.unique(np.random.uniform(low=0, high=Ntracks, size=(Ntracks_to_plot)).astype(int))
        pos = pos[:,idxt,:]
        Ntracks = idxt.shape[0]

    CoM = np.mean(pos, axis=1)

    for j in range(Ncolors):
        
        xs, ys, zs = [], [], []
        for i in range(Ntracks)[j::Ncolors]:
            xs.extend( pos[:,i,0]-CoM[:,0] )
            ys.extend( pos[:,i,1]-CoM[:,1] )
            zs.extend( pos[:,i,2]-CoM[:,2] )
            xs.append( np.nan )
            ys.append( np.nan )
            zs.append( np.nan )

        ax.plot(xs, ys, zs=zs, color=color[j], linewidth=linewidth, alpha=alpha)

    #get limits
    xmin = np.min(pos[0,:,0]-CoM[0,0])
    xmax = np.max(pos[0,:,0]-CoM[0,0])
    ymin = np.min(pos[0,:,1]-CoM[0,1])
    ymax = np.max(pos[0,:,1]-CoM[0,1])
    zmin = np.min(pos[0,:,2]-CoM[0,2])
    zmax = np.max(pos[0,:,2]-CoM[0,2])


    ax.grid(False)
    ax.set_axis_off()
    ax.set_facecolor('k')

    ax.view_init(elev=60, azim=0)

    shrink_factor = 0.5
    ax.set_xlim([shrink_factor*xmin, shrink_factor*xmax])
    ax.set_ylim([shrink_factor*ymin, shrink_factor*ymax])
    ax.set_zlim([shrink_factor*zmin, shrink_factor*zmax])

#labels
txt1 = fig.text(0.025, 0.75, 'GAS'  , horizontalalignment='center', verticalalignment='center', fontsize=35, color='lightgrey', fontweight='bold', zorder=10, rotation=90)
txt2 = fig.text(0.025, 0.25, 'STARS', horizontalalignment='center', verticalalignment='center', fontsize=35, color='lightgrey', fontweight='bold', zorder=10, rotation=90)

txt3 = fig.text(0.25, 0.05, 'OLD'  , horizontalalignment='center', verticalalignment='center', fontsize=35, color='lightgrey', fontweight='bold', zorder=10)
txt4 = fig.text(0.75, 0.05, 'YOUNG', horizontalalignment='center', verticalalignment='center', fontsize=35, color='lightgrey', fontweight='bold', zorder=10)

txt1.set_path_effects([PathEffects.withStroke(linewidth=15, foreground='k')])
txt2.set_path_effects([PathEffects.withStroke(linewidth=15, foreground='k')])
txt3.set_path_effects([PathEffects.withStroke(linewidth=15, foreground='k')])
txt4.set_path_effects([PathEffects.withStroke(linewidth=15, foreground='k')])


plt.tight_layout()
fig.savefig('mosaic.png', dpi=300, bbox='tight')
plt.cla()


```

_Press the tag below to see more examples_
