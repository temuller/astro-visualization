+++
# Beginning of HEADER
# This is a Markdown file!
title = "Galactic infall"

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

Caption: The plots shows the trajectories followed by all stars that end up in a galaxy. The image is created from a zoom-in hydrodynamical simulation part of the ZOMG suite.

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
from mpl_toolkits.mplot3d import Axes3D
import sys

model = int(sys.argv[1])

Ncolors=10
linewidth=1
alpha=0.1

Ntracks_to_plot = 2000  #-1 to use all

pos = np.load("tracks_stars_model%i.npy"%model)

Nsnaps, Ntracks, _ = pos.shape

if((Ntracks_to_plot > 0) and (Ntracks_to_plot < Ntracks)):
    idxt = np.unique(np.random.uniform(low=0, high=Ntracks, size=(Ntracks_to_plot)).astype(int))
    pos = pos[:,idxt,:]
    Ntracks = idxt.shape[0]

CoM = np.mean(pos, axis=1)

fig = plt.figure(figsize=(15.748,15.748))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace = 0.0, hspace = 0.0)

cmaps_name = 'gnuplot2'

color = cmaps.get_cmap(cmap_name)( np.linspace(0.0, 1.0, Ncolors, endpoint=True) )

for j in range(Ncolors):
    
    Nbeg = 0

    xs, ys, zs = [], [], []
    for i in range(Ntracks)[j::Ncolors]:
        xs.extend( pos[Nbeg:-1,i,0]-CoM[Nbeg:-1,0] )
        ys.extend( pos[Nbeg:-1,i,1]-CoM[Nbeg:-1,1] )
        zs.extend( pos[Nbeg:-1,i,2]-CoM[Nbeg:-1,2] )
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

shrink_factor = 0.2
ax.set_xlim([shrink_factor*xmin, shrink_factor*xmax])
ax.set_ylim([shrink_factor*ymin, shrink_factor*ymax])
ax.set_zlim([shrink_factor*zmin, shrink_factor*zmax])

fig.savefig('single_model%i_%s.png'%(model, cmap_name), dpi=300, bbox='tight')
plt.cla()

```

_Press the tag below to see more examples_
