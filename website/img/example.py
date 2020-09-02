def RS_plot_fit(color,mag,mur,paramRS,prob_weights=None,color_weights=None,maglim=25,labely=r'$g-r$',labelx=r'$r$',Name="RM",zcls=0.1,savedir='../graphs/RS/'):
    
    ## Set up the figure
    nullfmt = NullFormatter()         # no labels

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.12]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.clf()
    plt.figure(figsize=(16, 14))

    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    axScatter = plt.axes(rect_scatter)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    ylmin,ylmax = (mur-0.9), (mur+0.6)
    
    xmin = np.where(mag.min()<17,15.5,16.5)
    xlmin,xlmax = (maglim-5.,maglim+1.)
    # xlmin,xlmax = (mag.mean()-2*mag.std()-1.5),(24.)

    blue, red = '#024794','#AF2B2F'

    ## get the RS vector
    slope, intercept,sigr = paramRS
    mag_vec = np.arange(xlmin,xlmax+0.01,0.01)
    RS = slope*mag_vec+intercept

    
    # ------> Do the scatter plot
    c = (color_weights == None)&(color_weights < -1)&(color_weights > 1)
    color_weights[c] = 0.05
    
    top = cm.get_cmap('RdBu_r', 128)
    midle = cm.get_cmap('gray')
    bottom = cm.get_cmap('RdBu', 128)
    newcolors = np.vstack((top(np.linspace(0., 0.45, 128)),midle(np.linspace(0.2,0.3,8)),midle(np.linspace(0.3,0.2,8)),
                        bottom(np.linspace(0.45, 0., 128))))
    mycmp = ListedColormap(newcolors, name='RdGrBu')
    
    # rdmp = ListedColormap(top(np.linspace(0.5, 1., 128)),name='Rd')
    # mycmap = ListedColormap(sns.color_palette("RdBu_r", 7).as_hex())
    
    axScatter.plot(mag_vec,RS,color=red,linestyle='--',label='Best Fit RS')
    axScatter.axvline(maglim,linestyle='--',linewidth=2.,color=blue,label='$mag_{lim} = %.1f$'%(maglim))
    axScatter.scatter(mag, color,c=color_weights,s=120*(prob_weights)**(2)+0.01,alpha=0.7,cmap=mycmp,label=r'$P_{mem}$')
    axScatter.set_xlabel(labelx)
    axScatter.set_ylabel(labely)
    axScatter.set_xlim((xlmin,xlmax))
    axScatter.set_ylim((ylmin,ylmax)) 
    
    #make a legend:
    legendSizes = [0.1,0.5, 1.0]
    for lS in legendSizes:
        plt.scatter([], [],s=100*(lS)**(2)+0.01,c='gray',alpha=0.6,label='$ %.1f$'%(lS))
    axScatter.legend()
    axScatter.plot(mag_vec,RS+2*sigr*np.ones_like(mag_vec),color='k',linestyle='--')
    axScatter.plot(mag_vec,RS-2*sigr*np.ones_like(mag_vec),color='k',linestyle='--')
    # h, l = plt.gca().get_legend_handles_labels()
    # plt.legend(h[0:], l[0:], borderpad=1,frameon=True, framealpha=0.3, edgecolor="k", facecolor="w")
    
    # ------> Do the vertical histogram
    yvec = np.linspace(ylmin,ylmax,1000)
    ybins = np.arange(ylmin, ylmax + 0.075, 0.075)
    width=np.diff(ybins)
    
    axHisty.hist(color, bins=ybins,weights=prob_weights,
                edgecolor='white',linewidth=1.2,align='mid',color='gray',
                orientation='horizontal',alpha=1.0,histtype='bar',label=r'$P_{mem} \times N_{gal}$')
    
    axHisty.legend()
    
    # ------> Do the horizontal histogrammag.max()
    binwidth = 0.15
    xbins = np.arange(xlmin,xlmax + 0.5, 0.5)
    axHistx.hist(mag, bins=xbins,weights=prob_weights, edgecolor='white',linewidth=1.2,align='mid',color=blue,alpha=0.8,histtype='bar')
    axHistx.set_title(Name+' at z=%.3f'%(zcls))
    axHistx.legend()
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())

    # h, l = plt.gca().get_legend_handles_labels()
    # # axScatter.legend(h[1:], l[1:], loc=0, labelspacing=0.5,frameon=True, framealpha=0.3, edgecolor="gray", facecolor="lightgray")
    # plt.legend(h[1:], l[1:], labelspacing=0.5,loc='upper left', borderpad=1,title=r'$P_{mem}$',bbox_to_anchor=(0.2,0.30,1.,1.),frameon=True, framealpha=0.3, edgecolor="gray")

    ## Save 
    save=labely.split('$')[1]
    out_name = savedir+str(Name)+'_RS_Fit_%s.png'%(save)
    plt.savefig(out_name)
    # plt.show()
    plt.clf()
