import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .PlotPlanet import PlotPlanetXY
from .GCPM import GCPM

def PlotEqSlice(Date,ut,Parameter='ne',Rmax=10.0,dR=0.5,Kp=1.0,fig=None,
		maps=[1,1,0,0],zlog=True,cmap='gnuplot',scale=None,Verbose=False):
	'''
	Plots the GCPM model in the equatorial plane.
	
	Inputs
	======
	Date : int
		Date(s) in format yyyymmdd
	ut : float
		Time(s) in hours from beginning of day where 
		ut = hh + mm/60.0 + ss/3600.0
	Parameter : str
		'ne'|'nH'|'nHe'|'nO'
	Rmax : float
		Limits of the plot
	dR : float
		Size of bins on plot
	Kp : float
		Kp index (or indices)
	fig : object
		This should be either None (to create a new figure), a matplotlib.pyplot
		object (to add a new set of axes to an existing plot) or an 
		instance of matplotlib.pyplot.Axes in order to add to an existing
		set of axes.
	maps : list/tuple
		This will determine the position of the subplot on the figure.
	zlog : bool
		If True - the color scale will be logarithmic
	cmap : str
		String to say which colormap to use.
	scale : None or list/tuple
		If None - scale will be generated automatically, otherwise set 
		scale = [minimum,maximum]
	Verbose : bool
		If True, model calculation progress will be displayed	
	
	
	
	'''
	
	#create a grid of points to calculate the model at
	nR = 2*np.int32(Rmax/dR)
	xe = np.linspace(-Rmax,Rmax,nR+1)
	ye = xe
	xc = xe[:-1] + 0.5*dR
	yc = ye[:-1] + 0.5*dR
	xe,ye = np.meshgrid(xe,ye)
	xc,yc = np.meshgrid(xc,yc)
	zc = np.zeros(xc.shape)
	
	#calculate the model
	m = GCPM(xc,yc,zc,Date,ut,Kp=Kp,Verbose=Verbose)
	
	#get the color bar label
	inf = {	'ne' : (m[0],'$n_e$ (cm$^{-3}$)'),
			'nH' : (m[0],'$n_H$ (cm$^{-3}$)'),
			'nHe' : (m[0],'$n_He$ (cm$^{-3}$)'),
			'nO' : (m[0],'$n_O$ (cm$^{-3}$)')}
	data,zlabel = inf[Parameter]
	data = data.reshape(xc.shape)

	if zlog:
		norm = colors.LogNorm()
	else:
		norm = colors.Normalize()	
	
	
	#get the scale limits
	if scale is None:
		if zlog:
			scale = [np.nanmin(data[data > 0]),np.nanmax(data)]
		else:
			scale = [np.nanmin(data),np.nanmax(data)]
		
	

	#create the plot window
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		ax.set_xlim([Rmax,-Rmax])
		ax.set_ylim([-Rmax,Rmax])
		ax.set_aspect(1.0)
	else:
		ax = fig		
		
	#plot the mesh
	sm = ax.pcolormesh(ye,xe,data,cmap=cmap,norm=norm,vmin=scale[0],vmax=scale[1])

	#plot the planet
	PlotPlanetXY(ax)


	#sort the axis labels
	ax.set_ylabel('$x_{SM}$ ($R_E$)')
	ax.set_xlabel('$y_{SM}$ ($R_E$)')	
	
	

	#colorbar
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(sm,cax=cax) 
	cbar.set_label(zlabel)

	return ax
