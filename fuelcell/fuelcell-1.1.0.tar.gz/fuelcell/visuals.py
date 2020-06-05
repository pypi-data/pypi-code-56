import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

import utils
import datums

def testfun():
	print('haddock')

def plot_cv(data=None, labels=None, line=True, scatter=False, errs=False,
				current_column=1, potential_column=0, err_column=3,
				xunits='V', yunits=r'$mA/cm^2$',
				export_name=None, export_type='png', fig_kw={}, err_kw={}, **plot_kw):
	if not utils.check_dict(data):
		data = {'key':data}
	labels = check_labels(data, labels)
	fig, ax = plt.subplots(**fig_kw)
	for l, df in zip(labels, list(data.values())):
		df.columns = utils.check_labels(df)
		x = datums.find_col(df, 'potential', potential_column)
		y = datums.find_col(df, 'current', current_column)
		yerr = check_errs(errs, df, 'current_err', err_column, len(y))
		plotter(ax, x, y, yerr, l, line, scatter, errs, err_kw, **plot_kw)
	if len(data) > 1:
		ax.legend(loc='best')
	ax.set_xlabel(build_axlabel('Potential', xunits))
	ax.set_ylabel(build_axlabel('Current Density', yunits))
	if export_name:
		fig_saver(export_name, export_type)
	return fig, ax


def polcurve(data=None, labels=None, line=True, scatter=True, errs=False,
				current_column=0, potential_column=1, err_column=3,
				xunits=r'$mA/cm^2$', yunits='V',
				export_name=None, export_type='png', fig_kw={}, err_kw={}, **plot_kw):
	if not utils.check_dict(data):
		data={'key':data}
	labels = check_labels(data, labels)
	fig, ax = plt.subplots(**fig_kw)
	for l, df in zip (labels, list(data.values())):
		df.columns = utils.check_labels(df)
		x = datums.find_col(df, 'current', current_column)
		y = datums.find_col(df, 'potential', potential_column)
		yerr = check_errs(errs, df, 'potential_err', err_column, len(y))
		plotter(ax, x, y, yerr, l, line, scatter, errs, err_kw, **plot_kw)
	if len(data) > 1:
		ax.legend(loc='best')
	ax.set_xlabel(build_axlabel('Current Density', xunits))
	ax.set_ylabel(build_axlabel('Potential', yunits))
	if export_name:
		fig_saver(export_name, export_type)
	return fig, ax

def plot_cp_raw(data=None, labels=None, line=False, scatter=True, errs=False,
					current_column=2, potential_column=1,time_column=0, err_column=(4,5),
					xunits='s', yunits=('mA', 'V'),
					export_name=None, export_type='png', fig_kw={}, err_kw={}, **plot_kw):
	if not utils.check_dict(data):
		data = {'key': data}
	labels = check_labels(data, labels)
	fig, ax1 = plt.subplots(**fig_kw)
	ax2 = ax1.twinx()
	color1 = 'tab:red'
	color2 = 'tab:blue'
	for l, df in zip (labels, list(data.values())):
		x = datums.find_col(df, 'time', time_column)
		y1 = datums.find_col(df, 'potential', potential_column)
		y2 = datums.find_col(df, 'current', current_column)
		yerr1 = check_errs(errs, df, 'current_err', err_column[0], len(y1))
		yerr2 = check_errs(errs, df, 'potential_err', err_column[1], len(y2))
		plotter(ax1, x, y1, yerr1, l, line, scatter, errs, err_kw, s=1, c=color1, **plot_kw)
		plotter(ax2, x, y2, yerr2, l, line, scatter, errs, err_kw, s=1, c=color2, **plot_kw)
	if len(data) > 1:
		ax1.legend(loc='best')
	# color = 'tab:red'
	ax1.set_xlabel(build_axlabel('Time', xunits))
	ax1.set_ylabel(build_axlabel('Current Density', yunits[0]))
	ax2.set_ylabel(build_axlabel('Potential', yunits[1]))
	ax1.tick_params(axis='y', labelcolor=color1)
	ax2.tick_params(axis='y', labelcolor=color2)
	if export_name:
		fig_saver(export_name, export_type)
	return fig, (ax1, ax2)

def build_axlabel(base, units):
	return base + ' [' + units + ']'

def check_errs(errs, df, err_name, err_col, count):
	if errs:
		try:
			err = datums.find_col(df, err_name, err_col)
		except:
			err = np.zeros(count)
			warnings.warn('Unable to use the specified error values', UserWarning)
	else:
		err = np.zeros(count)
	return err

def check_labels(data, labels):
	if labels and (len(labels) != len(data)):
		labels = list(data.keys())
		warnings.warn('labels and data must have the same length. Using default labels instead of specified labels', UserWarning)
	elif labels is None:
		labels = list(data.keys())
	return labels

def fig_saver(export_name, export_type):
	if '.' not in export_name:
		export_type = export_type.replace('.','')
		export_name = export_name + '.' + export_type
	plt.savefig(export_name, bbox_inches='tight')

def plotter(ax, x, y, e, l, line, scatter, errs, err_kw, **plot_kw):
	if errs:
		if 'elinewidth' not in err_kw:
			err_kw['elinewidth'] = 0.5
		if 'capthick' not in err_kw:
			err_kw['capthick'] = 0.5
		if 'capsize' not in err_kw:
			err_kw['capsize'] = 3
		if 'marker' not in plot_kw:
			plot_kw['marker'] = '.'

		if line and scatter:
			ax.errorbar(x, y, e, label=l, **err_kw, **plot_kw)
		elif line:
			plot_kw.pop('marker')
			ax.errorbar(x, y, e, label=l, **err_kw, **plot_kw)
		else:
			plot_kw['ls'] = ''
			ax.errorbar(x, y, e, label=l, **err_kw, **plot_kw)
	else :
		if line and scatter:
			ax.plot(x, y, marker='.', label=l, **plot_kw)
		elif line:
			ax.plot(x, y, label=l, **plot_kw)
		else:
			ax.scatter(x, y, marker='*', label=l, **plot_kw)