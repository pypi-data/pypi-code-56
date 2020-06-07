import requests
import logging
import time
import urllib.parse
import json
import datetime
from airbornerf import jsog
from collections import OrderedDict

class Client:

	server_url = None
	xsrf_token = None
	logger = logging.getLogger("airbornerf.Client")

	def __init__(self, server_url):
		self.server_url = server_url
		self.session = requests.Session()
		self.logger.setLevel(logging.DEBUG)

	def _response_check(self, response):

		if response.status_code != requests.codes.ok:
			self.logger.error("Request failed: HTTP " + str(response.status_code))
			self.logger.error(response.text)
			raise RuntimeError("API request failed: HTTP " + str(response.status_code))

	def _response_check_json(self, response):

		self._response_check(response)
		jesponse = response.json()
		if jesponse['success'] != True:
			self.logger.error("Request failed: success is False")
			self.logger.error(jesponse)
			raise RuntimeError("API request failed: {} ({})".format(jesponse['errorMessage'], jesponse['errorCode']))
		return jesponse

	def _get_file_url(self, name):

		return self.server_url + "/file/get/" + str(name)

	def wait_for_ganot_task(self, ganot_task_id, timeout=60):

		while True:
			gt = self.ganottask_get(ganot_task_id)
			if gt['state'] == 'succeeded':
				return gt
			elif gt['state'] == 'failed':
				self.logger.error("Ganot task {} failed!".format(ganot_task_id))
				self.logger.error(gt)
				raise RuntimeError("Ganot task {} failed!".format(ganot_task_id))
			time.sleep(3)
			timeout -= 3
			if timeout <= 0:
				raise RuntimeError("Timeout exceeded!")

	def wait_for_ganot_tasks(self, ganot_task_ids, timeout=300):

		while True:
			ganot_tasks = []
			for ganot_task_id in ganot_task_ids:
				ganot_tasks.append(self.ganottask_get(ganot_task_id))
			
			some_incomplete = False
			for gt in ganot_tasks:
				if gt['state'] != 'succeeded' and gt['state'] != 'failed':
					some_incomplete = True
					break

			if not some_incomplete:
				failed_ids = []
				for gt in ganot_tasks:
					if gt['state'] == 'failed':
						failed_ids.append(gt['id'])
				
				if len(failed_ids) > 0:
					self.logger.error("Ganot task(s) {} failed!".format(failed_ids))
					self.logger.error(ganot_tasks)
					raise RuntimeError("Ganot task(s) {} failed!".format(failed_ids))

				return ganot_tasks

			time.sleep(3)
			timeout -= 3
			if timeout <= 0:
				raise RuntimeError("Timeout exceeded!")

	def renew_xsrf_token(self):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}

		response = self.session.request("GET", self.server_url + "/session/csrf", data=payload, headers=headers).json()
		self.xsrf_token = response['token']

	def login(self, username, password):

		self.renew_xsrf_token()
		headers = {
			'Content-Type': "application/x-www-form-urlencoded",
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		payload = urllib.parse.urlencode({
			'username': username,
			'password': password,
			'platform': 'webapp',
			'platformVersion': '1.0',
			'apiLevel': '1'
		})
		response = self.session.request("POST", self.server_url + "/login", data=payload, headers=headers)
		self._response_check(response)
		self.renew_xsrf_token()

	def logout(self):
		headers = {
			'Content-Type': "application/x-www-form-urlencoded",
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		self.session.request("POST", self.server_url + "/logout", headers=headers)

	def download(self, url, filename=None):

		if filename == None: 
			filename = url.split('/')[-1]
			
		response = self.session.get(url, allow_redirects=True)
		open(filename, 'wb').write(response.content)

	def get_session_user(self):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}
		response = self.session.request("GET", self.server_url + "/session/user", data=payload, headers=headers)
		self._response_check(response)
		return response.json()

	def measurement_upload(self, format, name, filename):

		files = {'files': open(filename, 'rb') }
		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		response = self.session.request("POST", self.server_url + "/measurement/upload/{}/{}".format(format, urllib.parse.quote(name)), files=files, headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def measurement_activate(self, measurement_id):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST", self.server_url + "/measurement/activate/" + str(measurement_id), headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def measurement_statistics_for_measurement(self, measurement_id):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST", self.server_url + "/measurement/statisticsForMeasurement/" + str(measurement_id), headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def measurement_update(self, measurement_id, attributes):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		# attributes can have the properties: name (String) and preview (Bool).
		# Both are optional.
		payload = json.dumps(attributes)
		response = self.session.request("PATCH", self.server_url + "/measurement/" + str(measurement_id), data=payload, headers=headers)
		self._response_check(response)
		return response.json()

	def radiospace_get(self):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}
		response = self.session.request("GET", self.server_url + "/radiospace/get", data=payload, headers=headers)
		self._response_check(response)
		return response.json()

	def radiospace_statistics_for_file(self, format, radiospace_id, filename, point_in_time=None):

		files = {'files': open(filename, 'rb') }
		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		request_url = self.server_url + "/radiospace/statisticsForFile/{}/{}".format(format, radiospace_id)
		if point_in_time is not None:
			self.server_url + "/radiospace/statisticsForFile/{}/{}/{}".format(format, radiospace_id, point_in_time.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
		response = self.session.request("POST", request_url, files=files, headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def radiospace_statistics_for_path(self, radiospace_id, path, routing_mode="direct", interpolate=True, point_in_time=None):
		"""
		Run flight path statistics.
		:param radiospace_id: The radiospace in which to run the statistics.
		:param path: The flight path. An array of hashes containing "latitude", "longitude" and "altitude" keys.
		:param routing_mode:
		:param interpolate:
		:param point_in_time: If in the future, calculates the statistics for that time in the future. A datetime object
		:return:
		"""
		data = {
			"path": path,
			"routingMode": routing_mode,
			"interpolate": interpolate
		}
		if point_in_time is not None:
			data['pointInTime'] = point_in_time.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
		payload = json.dumps(data)

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST", self.server_url + "/radiospace/statisticsForPath/{}".format(radiospace_id), headers=headers, data=payload)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def radiospace_calculate(self, radiospace_id, west, north, east, south):

		headers = {
			'cache-control': "no-cache",
		}
		response_calculate = self.session.request("GET", self.server_url + "/radiospace/calculate/{}/{}/{}/{}/{}".format(radiospace_id, west, north, east, south), headers=headers)
		self._response_check_json(response_calculate)
		
		# Check which tilespecs should be calculated, thus get them first
		response_tilespecs = self.session.request("GET", self.server_url + "/geo/tilespecs/{}/{}/{}/{}".format(west, north, east, south), headers=headers)
		self._response_check(response_tilespecs)
		tilespecs = response_tilespecs.json()

		# Wait for backend to start processing
		task_ids = {}
		processing_started = False
		active_tiles = []
		sleep_time = 0.1
		timeout = 10

		while not processing_started:
			response_processing = self.session.request("GET", self.server_url + "/radiospace/{}/tiles/processing".format(radiospace_id), headers=headers)
			self._response_check(response_processing)
			active_tiles = response_processing.json()

			# Check if all tilespecs are processing
			for at in active_tiles:
				if at['tilespec'] in tilespecs:
					task_ids[at['tilespec']] = at['ganotTask']['id']

			if len(tilespecs) == len(task_ids.keys()):
				processing_started = True
			else:
				time.sleep(sleep_time)
				timeout -= sleep_time
				if timeout <= 0:
					processing_started = True
					self.logger.warning("Some requested tilespecs are not calculated")
					self.logger.warning("Requested tilespecs: {}".format(tilespecs))
					self.logger.warning("Radiospace calculation tasks: {}".format(task_ids))

		return list(task_ids.values())

	def radiospace_tiles_get(self, radiospace_id, west, north, east, south):

		headers = {
			'cache-control': "no-cache",
		}
		response = {}
		response_layers = self.session.request("GET", self.server_url + "/radiospace/{}/layer/all".format(radiospace_id), headers=headers)
		self._response_check(response_layers)
		for layer in response_layers.json():
			response_tiles = self.session.request("GET", self.server_url + "/radiospace/getTiles/{}/{}/{}/{}/{}".format(layer['id'], west, north, east, south), headers=headers)
			self._response_check(response_tiles)
			tiles_json = jsog.decode(response_tiles.json(object_pairs_hook=OrderedDict))

			for tile in tiles_json:
				if tile['layer']['type'] not in response:
					response[tile['layer']['type']] = []

				response[tile['layer']['type']].append({
					'id': tile['id'],
					'tilespec': tile['tilespec'],
					'url': self._get_file_url(tile['ref']),
					'updated': tile['updated'],
					'settings': tile['settings'],
					'layer': {
						'id': tile['layer']['id'],
						'type': tile['layer']['type'],
						'name': tile['layer']['name']
					}
				})

		return response

	def customflight_persist(self, ganot_task_id, name):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST", self.server_url + "/custom-flight/ganotTaskId/{}/name/{}/preview/false".format(ganot_task_id, urllib.parse.quote(name)), headers=headers)
		self._response_check(response)
		return response.json()

	def ganottask_get(self, ganot_task_id):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}
		response = self.session.request("GET", self.server_url + "/ganottask/get/" + str(ganot_task_id), data=payload, headers=headers)
		self._response_check(response)
		return response.json()

	def ganottask_abort(self, ganot_task_id):
		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
		}
		response = self.session.request("DELETE", self.server_url + "/ganottask/abort/{}".format(ganot_task_id), headers=headers)
		self._response_check_json(response)