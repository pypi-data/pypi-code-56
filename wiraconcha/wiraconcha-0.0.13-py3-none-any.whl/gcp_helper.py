from google.cloud import storage
from google.cloud import error_reporting
import os
import logging
import sys
import json
import time
from functools import wraps

error_client = error_reporting.Client()


def download_data(bucket_name, gcs_path, local_path, verbose=False):
	""" Downloads data from GCP bucket
	Args:
		bucket_name (STRING): bucket_name
		gcs_path (STRING): location of object inside bucket
		local_path (STRING): location where object will be saved
	Returns:
	"""
	if verbose:
		logging.info("Downloading gs://{}/{} to {}".format(bucket_name,
															gcs_path,
															local_path))
	bucket = storage.Client().bucket(bucket_name)
	blob = bucket.blob(gcs_path)
	blob.download_to_filename(local_path)


def upload_data(bucket_name, gcs_path, local_path, name=''):
	""" Uploads data from GCP bucket
	Args:
		bucket_name (STRING): bucket_name
		gcs_path (STRING): location of object inside bucket
		local_path (STRING): location where object will be saved
		name (STRING): option name of object
	Returns:
	"""
	bucket = storage.Client().bucket(bucket_name)
	if name:
		path = gcs_path + '/' + name
	else:
		path = gcs_path
	blob = bucket.blob(path)
	blob.upload_from_filename(local_path)
	logging.info("Uploaded {} to {}".format(local_path, path))


def load_data(df, sample=None):
	""" Prepares data by removing products with less than 15 occurences
		and splitting it into train and test with the 30% most recent events
		being the test set
	Args:
		df (PANDAS DATAFRAME):  Dataframe
		sample (INT): sample size if desired
	Returns:
		train (PANDAS DATAFRAME): 70% of orgional dataframe
		test (PANDAS DATAFRAME): 30% of orgional dataframe
	"""
	df = df.reset_index()
	if sample:
		df = df.sample(n=sample)
	dcounts = df.groupby('Description').count()
	dlist = dcounts[dcounts['index'] > 15].index.tolist()
	df = df[df['Description'].isin(dlist)]

	splitIndex = round(len(df) * .7)
	train = df[:splitIndex].copy()
	test = df[splitIndex:].copy()

	logging.info("train: {}   test: {}   Total: {}".format(len(train), len(test), len(df)))
	return train, test


def get_bucket_path(gcs_uri):
	""" divides uri into bucket and path
	Args:
		gcs_uri (STRING): Google cloud storage uri to object
	Returns:
		bucket_name (STRING): name of bucket
		gcs_path (STRING):  object path
	"""
	logging.info("gcs_uri: {}".format(gcs_uri))
	if not gcs_uri.startswith('gs://'):
		raise Exception('{} does not start with gs://'.format(gcs_uri))
	no_gs_uri = gcs_uri[len('gs://'):]
	first_slash_index = no_gs_uri.find('/')
	bucket_name = no_gs_uri[:first_slash_index]
	gcs_path = no_gs_uri[first_slash_index + 1:]
	return bucket_name, gcs_path


def setupLogger():
	""" properly sets up the logger depending on if the code is running
		on a cloud function or locally

		Args:
		Returns:
	"""
	logging.info(dict(os.environ))
	function_identity = os.environ.get('FUNCTION_IDENTITY', 'local')
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	root.info("function_identity: {}".format(function_identity))
	if function_identity == 'local':
		logging.StreamHandler(sys.stdout)


def get_project_id():
	""" Gets the project ID. It defaults to the project declared in the
		enviorment variable PROJECT but if it can't find it there it will
		try looking for a service account and take the project ID from there

		Args:
		Returns:
	"""
	service_acc_address = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)
	if service_acc_address:
		service_acc = open(service_acc_address, 'r').read()
		service_acc_project_id = json.loads(service_acc)['project_id']
	else:
		service_acc_project_id = None
	project_id = os.environ.get('PROJECT', service_acc_project_id)

	if service_acc_project_id != None and project_id != service_acc_project_id:
		logging.critical("Warning the project in ENV VAR PROJECT is \
			not the same as your service account project")

	return project_id


def raise_bug_error(error, message=''):
	""" Gets the project ID. It defaults to the project declared in the
		enviorment variable PROJECT but if it can't find it there it will
		try looking for a service account and take the project ID from there

		Args: error (Exception): The Exception causing error
			  message (STRING): A custom message to be preprended to the error
		Returns:
	"""
	msg = f"{message} {str(error)}"
	if message != '':
		logging.critical(message)
	logging.error(msg)
	# This line sends the error to the "Error Reporting" section of GCP console
	error_client.report(msg)


def function_event(func):
	"""Decorator for logging node execution time and event contents

		Args:
			func: Function to be executed.

		Returns:
			Decorator for logging the running time.

	"""

	@wraps(func)
	def with_time(event, context, **kwargs):
		setupLogger()
		log = logging.getLogger(__name__)

		logging.info(f"Event: {event}")
		logging.debug(f"Context: {context}")

		t_start = time.time()
		result = func(event, context, **kwargs)
		t_end = time.time()
		elapsed = t_end - t_start
		log.info("Running %r took %.2f seconds", func.__name__, elapsed)
		return result

	return with_time

def prep_function():
	"""A cold start setup process for cloud functions


		Returns:
			service (STRING): name of service
			project_id (STRING): name of GCP project
			stage (STRING): Enviorment stage

	"""
	setupLogger()
	service = os.environ.get('SERVICE', 'MCGMT')
	stage = os.environ.get('stage', 'dev')
	project_id = get_project_id()
	logging.info(f"Project: {project_id}  Stage: {stage}")
	return service, project_id, stage