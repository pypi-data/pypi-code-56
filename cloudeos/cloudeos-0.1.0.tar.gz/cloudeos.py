import requests
import json

'''
Api documention 
https://documenter.getpostman.com/view/2734345/SVmyQGv1?version=latest
'''


class API:


	def __init__(self, username, password):
		self.baseUrl = "https://api.cloudeos.com"
		self.loginUrl = self.baseUrl + "/v1/user/login"		
		self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
		self.data = {"reqion": 1, "id": "980f29c2-4cd8-417b-8566-f0745254d2e1"}
		data = {"username": username, "password": password}
		request = requests.post(self.loginUrl, headers=self.headers, data=data).json()
		if request["status"] == "success":
			self.token = request["data"]["token"]
			self.refreshtoken = request["data"]["refreshtoken"]
		else:
			print("Error:", request["message"])
		
		
	def get_refreshToken(self):
		url = self.baseUrl + "/v1/user/refreshtoken"
		data = {"refresh": self.token}
		request = request.post(url, headers=self.headers, data=data).json()
		if request["status"] == "success" and refresh["data"]["refresh"]:
			return request["data"]["refreshtoken"]
		else:
			print("Error:", request["message"])
			
			
	def get_accountDetail(self):
		url = self.baseUrl + "/v1/account/detail"
		headers = {"Authorization": "Bearer %s" % self.token}
		request = requests.get(url, headers=headers, data=self.data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
		
		
	def get_balance(self):
		url = self.baseUrl + "/v1/account/user_balance"
		headers = {
			"Authorization": "Bearer %s" % self.token,
			"Content-Type": "Bearer %s" % self.token
		}
		request = requests.get(url, headers=headers).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
		
		
	def list_all_servers(self):
		url = self.baseUrl + "/v1/server/list"
		headers = self.headers
		headers["Authorization"] = "Bearer %s" % self.token
		request = requests.get(url, headers=headers, data=self.data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])


	def create_server(self, name, region, package, image, hostname=None, ssh_keys=None, user_data=None, tags=[]):
		url = self.baseUrl + "/v1/server/create"
		data = {
			"name": name, 
			"region": region, 
			"package": package, 
			"image": image, 
			"hostname": hostname if hostname else name.lower()
		}
		parameters = {"ssh_keys":ssh_keys, "user_data":user_data, "tags":tags}
		for key, value in parameters.items():
			if value:
				data[key] = value
		headers = {
			'Authorization': 'Bearer %s' % self.token,
			'Content-Type': 'application/json'
		}
		request = requests.post(url, headers=headers, data=json.dumps(data)).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
		
		
	def destroy_server(self, id):
		url = self.baseUrl + "/v1/server/" + str(id) + "/destroy"
		headers = self.headers
		headers["Authorization"] = "Bearer %s" % self.token
		request = requests.delete(url, headers=headers).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
		
		
	def create_sshkey(self, name, public_key):
		url = self.baseUrl + "/v1/sshkey/create"
		data = json.dumps({
			"name": name, 
			"public_key": public_key
		})
		headers = {
			'Authorization': 'Bearer %s' % self.token,
			'Content-Type': 'application/json'
		}
		request = requests.post(url, headers=headers, data=data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
			
			
	def get_sshkeys(self):
		url = self.baseUrl + "/v1/sshkey/list"
		headers = {'Authorization': 'Bearer %s' % self.token}
		request = requests.get(url, headers=headers, data=self.data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
		
		
	def destroy_sshkey(self, fingerprint):
		url = self.baseUrl + "/v1/sshkey/destroy"
		headers = self.headers
		headers["Authorization"] = "Bearer %s" % self.token
		data = {"fingerprint": fingerprint}
		request = requests.delete(url, headers=headers, data=data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
			
		
	@classmethod
	def get_regions(cls):
		url = "https://api.cloudeos.com/v1/region/list"
		data = {"reqion": 1, "id": "980f29c2-4cd8-417b-8566-f0745254d2e1"}
		request = requests.get(url, data=data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
	
	
	@classmethod
	def get_packages(cls):
		url = "https://api.cloudeos.com/v1/package/list"
		data = {"reqion": 1, "id": "980f29c2-4cd8-417b-8566-f0745254d2e1"}
		request = requests.get(url, data=data).json()
		if request["status"] == "success":
			return request["data"]
		else:
			print("Error:", request["message"])
			
			
			