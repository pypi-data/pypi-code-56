import os, requests

class ForbiddenAccessException(Exception):
    def __init__(self, message):
        self.message = message

class UnauthorizedAccessException(Exception):
    def __init__(self, message):
        self.message = message

class Client:
    def __init__(self, domain=None, username=None, password=None, access_token=None):
        if domain != None:
            self.api_url = 'https://api.' + domain + '/'
        else:
            self.api_url = 'http://cdrive/'
        if access_token != None:
            self.access_token = access_token
            self.home = 'users/' + self.user_details()['username']
        elif (username != None and password != None):
            self.access_token = self.get_token(username, password)
            self.home = 'users/' + username
        elif 'COLUMBUS_ACCESS_TOKEN' in os.environ:
            self.access_token = os.environ['COLUMBUS_ACCESS_TOKEN']
            self.home = 'users/' + self.user_details()['username']
        else:
            self.access_token = self.get_token(os.environ['COLUMBUS_USERNAME'], os.environ['COLUMBUS_PASSWORD'])

    def get_token(self, username, password):
        response = requests.post(url= self.api_url + 'api-access-token/', data={'username': username, 'password': password})
        return response.json()['accessToken']

    def user_details(self):
        auth_header = 'Bearer ' + self.access_token
        response = requests.get(url= self.api_url + 'user-details/', headers={'Authorization': auth_header})
        if response.status_code == 401:
            raise UnauthorizedAccessException('Cannot identify user')
        return response.json()

    def upload(self, local_path, cdrive_path):
        if os.path.isdir(local_path):
            folder_name = os.path.basename(local_path)
            self.create_folder(cdrive_path, folder_name)
            for obj_name in os.listdir(local_path):
                self.upload(cdrive_path + '/' + folder_name, os.path.join(local_path, obj_name))
        else:
            file_arg = None
            f = open(local_path, 'rb')
            file_name = os.path.basename(local_path)
            file_arg = {'file': (file_name, f), 'path': (None, cdrive_path)}
            response = requests.post(self.api_url + 'upload/', files=file_arg, headers={'Authorization': 'Bearer ' + self.access_token})
            f.close()
            if response.status_code == 401:
                raise UnauthorizedAccessException(response.json()['message'])
            elif response.status_code == 403:
                raise ForbiddenAccessException(response.json()['message'])

    def create_file(self, cdrive_path, file_name, content):
        file_arg = {'file': (file_name, content), 'path': (None, cdrive_path)}
        response = requests.post(self.api_url + 'upload/', files=file_arg, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 401:
            raise UnauthorizedAccessException(response.json()['message'])
        elif response.status_code == 403:
            raise ForbiddenAccessException(response.json()['message'])

    def create_folder(self, cdrive_path, name):
        data = {
            'path': cdrive_path,
            'name': name
        }
        response = requests.post(self.api_url + 'create/', data=data, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 401:
            raise UnauthorizedAccessException(response.json()['message'])
        elif response.status_code == 403:
            raise ForbiddenAccessException(response.json()['message'])

    def list_detailed(self, cdrive_path):
        response = requests.get(self.api_url + 'list/?path=' + cdrive_path, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 401:
            raise UnauthorizedAccessException('Cannot identify user')
        elif response.status_code == 403:
            raise ForbiddenAccessException(response.json()['message'])
        elif response.status_code != 200:
            raise Exception('Error reading from CDrive')
        return response.json()

    def list(self, cdrive_path):
        return self.list_detailed(cdrive_path)['driveObjects'] 

    def list_files(self, cdrive_path, recursive=False):
        if recursive:
            return self.list_files_recursive(cdrive_path, '')
        else:
            files = []
            folder_details = self.list_detailed(cdrive_path)
            for dobj in folder_details['driveObjects']:
                if dobj['type'] == 'File':
                    files.append(dobj['name'])
            return files

    def list_files_recursive(self, cdrive_path, base_path):
        folder_details = self.list_detailed(cdrive_path)
        files = []
        for dobj in folder_details['driveObjects']:
            if dobj['type'] == 'Folder':
                files.extend(self.list_files_recursive(cdrive_path + '/' + dobj['name'], base_path + dobj['name'] + '/'))
            else:
                files.append(base_path + dobj['name'])
        return files

    def download_folder(self, cdrive_path, local_path):
        child_objs = self.list_detailed(cdrive_path)['driveObjects']
        folder_path = os.path.join(local_path, cdrive_path[cdrive_path.rfind('/')+1:])
        os.mkdir(folder_path)
        for cobj in child_objs:
            if cobj['type'] == 'Folder':
                download_folder(cdrive_path + '/' + cobj['name'], folder_path)
            else:
                download_file(cdrive_path + '/' + cobj['name'], folder_path)

    def download_file(self, cdrive_path, local_path):
        file_url = self.file_url(cdrive_path)
        name = cdrive_path[cdrive_path.rfind('/')+1:]
        response = requests.get(file_url)
        with open(os.path.join(local_path, name), 'wb') as f:
            f.write(response.content)

    def download(self, cdrive_path, local_path):
        parent_path = cdrive_path[:cdrive_path.rfind('/')]
        dobjs = self.list_detailed(parent_path)
        obj_it = filter(lambda x: x['name'] == cdrive_path[cdrive_path.rfind('/') + 1:], dobjs['driveObjects'])
        try:
            dobj = next(obj_it)
            if dobj['type'] == 'File':
                download_file(cdrive_path, local_path)
            else:
                download_folder(cdrive_path, local_path)
        except StopIteration:
            raise ForbiddenAccessException('Requested object does not exist or you do not have permission to access it')

    def file_url(self, cdrive_path):
        response = requests.get(self.api_url + 'download/?path=' + cdrive_path, headers={'Authorization':'Bearer ' + self.access_token})
        if response.status_code == 403:
            raise ForbiddenAccessException('Requested object does not exist or you do not have permission to access it')
        elif response.status_code == 401:
            raise UnauthorizedAccessException('Cannot identify user')
        elif response.status_code != 200:
            raise Exception('Error in Download')
        else:
            return response.json()['download_url']

    def delete(self, cdrive_path):
        response = requests.delete(self.api_url + 'delete/?path=' + cdrive_path, headers={'Authorization':'Bearer ' + self.access_token})
        if response.status_code == 401:
            raise UnauthorizedAccessException('Cannot identify user')
        elif response.status_code == 403:
            raise ForbiddenAccessException('The object does not exist or you do not have permission to delete it')
        elif response.status_code != 204:
            raise Exception('Error reading from CDrive')

    def share(self, cdrive_path, permission, target_name='', target_type='user'):
        data = {
            'path': cdrive_path,
            'permission': permission,
            'targetType': target_type,
            'name': target_name
        }
        response = requests.post(self.api_url + 'share/', data=data, headers={'Authorization': 'Bearer ' + self.access_token})

    def install_app(self, app_url):
        response = requests.post(self.api_url + 'install-application/', data={'app_docker_link': app_url}, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 201:
            app_name = response.json()['appName']
            while(True):
                res = requests.get(self.api_url + 'app-status/?app_name=' + app_name, headers={'Authorization': 'Bearer ' + self.access_token})
                if res.status_code == 200 and res.json()['appStatus'] == 'Available':
                    break
            return app_name

    def app_token(self, app_name):
        response = requests.post(self.api_url + 'app-token/', data={'app_name': app_name}, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 200:
            return response.json()['app_token']
