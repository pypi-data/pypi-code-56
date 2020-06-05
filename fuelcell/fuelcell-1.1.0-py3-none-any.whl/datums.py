import numpy as np
import pandas as pd
import os
import re

import utils

dlm_default = utils.dlm_default
col_default_labels = {'current':'i', 'potential':'v', 'time':'t',
						'current_err':'i_sd', 'potential_err':'v_sd'}
col_default_ids = {'current':1, 'potential':2, 'time':0,
					'current_err':2, 'potential_err':3}
ref_electrodes = {'she':0, 'sce':0.241}


def testfun():
	print('bianca')

def ca_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	data = load_data(filename, folder, pattern, 'ca', filetype, delimiter)
	return data

def ca_process(data=None, area=5, current_column=1, potential_column=2, threshold=5, min_step_length=50, pts_to_average=300, pyramid=False, reference=None, **kwargs):
	if data is None:
		data = ca_raw(**kwargs)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		ca_processed = process_steps(df, area, current_column, potential_column, threshold, min_step_length, pts_to_average, pyramid, reference, 'ca')
		newdata[k] = ca_processed
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def cp_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	data = load_data(filename, folder, pattern, 'cp', filetype, delimiter)
	return data

def cp_process(data=None, area=5, current_column=1, potential_column=2, threshold=5, min_step_length=25, pts_to_average=300, pyramid=True, reference=None, **kwargs):
	if data is None:
		data = cp_raw(**kwargs)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		cp_processed = process_steps(df, area, current_column, potential_column, threshold, min_step_length, pts_to_average, pyramid, reference, 'cp')
		newdata[k] = cp_processed
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def cv_raw(filename=None, folder=None, pattern='', filetype='', delimiter=dlm_default):
	data = load_data(filename, folder, pattern, 'cv', filetype, delimiter)
	return data

def cv_process(data=None, area=5, current_column=1, potential_column=0, **kwargs):
	if data is None:
		data = cv_raw(**kwargs)
	if not utils.check_dict(data):
		data = {'key': data}
	newdata = dict()
	for k, df in data.items():
		current = find_col(df, 'current', current_column)
		current = current / area
		potential = find_col(df, 'potential', potential_column)
		cv_processed = pd.DataFrame({'i':current,'v':potential})
		newdata[k] = cv_processed
	if len(newdata) == 1:
		newdata = list(newdata.values())[0]
	return newdata

def array_apply(arr, func, **kwargs):
	result = [func(a, **kwargs) for a in arr]
	return np.array(result)

def avg_last_pts(arr, numpts=300):
	if type(arr) == list:
		arr = np.array(arr)
	avg = np.mean(arr[-numpts:])
	return avg

def find_col(data, col_type, label=None):
	default_label = col_default_labels[col_type]
	default_id = col_default_ids[col_type]
	newdf = data.copy()
	newdf.columns = utils.check_labels(newdf)
	if default_label in newdf.columns:
		col = newdf[default_label]
	elif label:
		if utils.check_str(label):
			col = newdf[label]
		else:
			col = newdf.iloc[:,label]
	else:
		col = newdf.iloc[:, default_id]
	return col

def find_steps(arr, threshold=5):
	if type(arr) == list:
		arr = np.array(arr)
	diffs = np.abs(np.diff(arr))
	splits = np.where(diffs > threshold)[0] + 1
	return splits

def load_data(filename=None, folder=None, pattern='', expttype='', filetype='', delimiter=dlm_default):
	data = None
	if filename:
		name, data = utils.read_file(filename, delimiter)
	else:
		if folder:
			dirpath = os.path.realpath(folder)
		else:
			dirpath = os.getcwd()
		if expttype and not pattern:
			pattern = r'.*' + expttype + r'.*'
		files = utils.get_files(dirpath, pattern, filetype)
		data = dict()
		for f in files:
			path = os.path.join(dirpath, f)
			name, df = utils.read_file(path, delimiter)
			if df is not None:
				data[name] = df
		if len(data) == 1:
			data = list(data.values())[0]
	return data

def process_steps(data, area, current_column, potential_column, threshold, min_step_length, pts_to_average, pyramid, reference, expttype='cp'):
	current = np.array(find_col(data, 'current', current_column))
	potential = np.array(find_col(data, 'potential', potential_column))
	if expttype == 'ca':
		split_pts = find_steps(potential, threshold=threshold)
	elif expttype == 'cp':
		split_pts = find_steps(current, threshold=threshold)
	current_steps = split_and_filter(current, split_pts, min_length=min_step_length)
	potential_steps = split_and_filter(potential, split_pts, min_length=min_step_length)
	current_avg = array_apply(current_steps, avg_last_pts, numpts=pts_to_average)
	potential_avg = array_apply(potential_steps, avg_last_pts, numpts=pts_to_average)
	current_std = array_apply(current_steps, std_last_pts, numpts=pts_to_average)
	potential_std = array_apply(potential_steps, std_last_pts, numpts=pts_to_average)
	if pyramid:
		sort_idx = np.argsort(current_avg)
		current_avg = current_avg[sort_idx]
		potential_avg = potential_avg[sort_idx]
		current_std = current_std[sort_idx]
		potential_std = potential_std[sort_idx]
		if expttype == 'ca':
			split_pts = find_steps(potential_avg, threshold=2)
		elif expttype == 'cp':
			split_pts = find_steps(current_avg, threshold=2)
		current_steps = split_and_filter(current_avg, split_pts)
		potential_steps = split_and_filter(potential_avg, split_pts)
		current_std_steps = split_and_filter(current_std, split_pts)
		potential_std_steps = split_and_filter(potential_std, split_pts)
		current_avg = array_apply(current_steps, np.mean)
		potential_avg = array_apply(potential_steps, np.mean)
		current_std = array_apply(current_std_steps, std_agg)
		potential_std = array_apply(potential_std_steps, std_agg)
	current_avg = current_avg / area
	current_std = current_std / area
	if reference:
		if utils.check_str(reference):
			reference = reference.lower()
			try:
				potential_avg += ref_electrodes[reference]
			except KeyError:
				pass
		elif utils.check_float(reference) or utils.check_int(reference):
			potential_avg += reference
	processed = pd.DataFrame({'i':current_avg, 'v':potential_avg, 'i_sd':current_std, 'v_sd':potential_std})
	return processed

def split_and_filter(arr, split_pts, min_length=0):
	if type(arr) == list:
		arr = np.array(arr)
	steps = np.split(arr, split_pts)
	steps_tokeep = np.array([s for s in steps if len(s) > min_length])
	return steps_tokeep

def std_agg(std_arr):
	return np.sqrt(np.sum(std_arr**2))

def std_last_pts(arr, numpts=300):
	if type(arr) == list:
		arr = np.array(arr)
	std = np.std(arr[-numpts:], ddof=1)
	return std