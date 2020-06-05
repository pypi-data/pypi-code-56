import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .PlotPlanet import PlotPlanetXZ
from .GCPM import GCPM

def PlotMLTSlice(MLT,Date,ut,Parameter='ne',Rmax=10.0,dR=0.5,Kp=1.0,fig=None,
		maps=[1,1,0,0],zlog=True,cmap='gnuplot',scale=None,Verbose=False):
	'''
	Plots the GCPM model in the equatorial plane.
	
	Inputs
	======
	MLT: float
		local time to calculate for
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
	ze = np.linspace(-Rmax,Rmax,nR+1)
	rhoe = ze
	zc = ze[:-1] + 0.5*dR
	rhoc = rhoe[:-1] + 0.5*dR
	mlt = (MLT - 12.0)* np.pi/12.0
	rhoe,ze = np.meshgrid(rhoe,ze)
	rhoc,zc = np.meshgrid(rhoc,zc)

	xc = rhoc*np.cos(mlt)
	yc = rhoc*np.sin(mlt)

	#work out which side the MLT is on the plot
	leftlab = '{:4.1f} MLT'.format(MLT + 12.0 % 24.0)
	rightlab = '{:4.1f} MLT'.format(MLT % 24.0)

	
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
		ax.set_ylim([Rmax,-Rmax])
		ax.set_xlim([-Rmax,Rmax])
		ax.set_aspect(1.0)
	else:
		ax = fig		
		
	#plot the mesh
	sm = ax.pcolormesh(rhoe,ze,data,cmap=cmap,norm=norm,vmin=scale[0],vmax=scale[1])

	#plot the planet
	PlotPlanetXZ(ax,NoBlack=True)


	#sort the axis labels
	ax.set_xlabel(r'$\rho_{SM}$ ($R_E$)')
	ax.set_ylabel('$z_{SM}$ ($R_E$)')	
	
	

	#colorbar
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	cbar = plt.colorbar(sm,cax=cax) 
	cbar.set_label(zlabel)

	return ax,xc,yc,zc,m
