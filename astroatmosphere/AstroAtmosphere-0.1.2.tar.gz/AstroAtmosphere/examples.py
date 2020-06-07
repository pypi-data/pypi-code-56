#!/usr/bin/env Python3
from .ciddorModel import Observatory
from .refractionModels import refraction
from .dispersionModels import dispersion
'''
	Author: Joost van den Born
	Some functions for quick testing.
'''


def quick_refractive_index(l, conditions='STANDARD'):
	if conditions == 'STANDARD':
		# Parameters at Cerro Armazones
		T   = 288.15    # k
		P   = 101325    # Pa
		H   = 0.0
		xc  = 450       # ppm
		lat = 0  		# degrees
		h   = 0     	# m
		

	elif conditions == 'CERRO_ARMAZONES':
		# Parameters at Cerro Armazones
		T   = 279.65    # k
		P   = 71200     # Pa
		H   = 0.22
		xc  = 450       # ppm
		lat = -24.5983  # degrees
		h   = 3064      # m
		

	# Initializing dispersion model
	at  = Observatory()

	# Calculating indices of refraction for l
	n 	= at.n_tph(l=l, T=T, p=P, RH=H, xc=xc)
	return n

def quick_refraction(l, z, conditions='STANDARD'):
	if conditions == 'STANDARD':
		# Parameters at Cerro Armazones
		T   = 288.15    # k
		P   = 101325    # Pa
		H   = 0.0
		xc  = 450       # ppm
		lat = 0  		# degrees
		h   = 0     	# m
		

	elif conditions == 'CERRO_ARMAZONES':
		# Parameters at Cerro Armazones
		T   = 279.65    # k
		P   = 71200     # Pa
		H   = 0.22
		xc  = 450       # ppm
		lat = -24.5983  # degrees
		h   = 3064      # m

	# Initializing dispersion model
	at  = Observatory()

	# Calculating indices of refraction for l
	n 	= at.n_tph(l=l, T=T, p=P, RH=H, xc=xc)

	# Density of the atmosphere (following CIPM-81/91 equations)
	rho = at.rho(p=P, T=T, RH=H, xc=xc)

	# Initializing refraction model and setting the reduced height
	ref = refraction(lat, h)
	ref.setReducedHeight(P, rho)
	return ref.cassini(n, z)

def quick_dispersion(l1, l2, z, conditions='STANDARD'):
	if conditions == 'STANDARD':
		# Parameters at Cerro Armazones
		T   = 288.15    # k
		P   = 101325    # Pa
		H   = 0.0
		xc  = 450       # ppm
		lat = 0  		# degrees
		h   = 0     	# m
		

	elif conditions == 'CERRO_ARMAZONES':
		# Parameters at Cerro Armazones
		T   = 279.65    # k
		P   = 71200     # Pa
		H   = 0.22
		xc  = 450       # ppm
		lat = -24.5983  # degrees
		h   = 3064      # m

	# Initializing dispersion model
	at  = Observatory()

	# Calculating indices of refraction for l1 and l2
	n1 	= at.n_tph(l=l1, T=T, p=P, RH=H, xc=xc)
	n2 	= at.n_tph(l=l2, T=T, p=P, RH=H, xc=xc)

	# Density of the atmosphere (following CIPM-81/91 equations)
	rho = at.rho(p=P, T=T, RH=H, xc=xc)

	# Initializing refraction model and setting the reduced height
	disp = dispersion(lat, h)
	disp.setReducedHeight(P, rho)
	return disp.cassini(n1, n2, z)