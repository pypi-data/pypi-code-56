import time
import random
import requests
import json
import string
import os
from jinja2 import Template
from cvapianalyser import CommunityEdition
from openapispecdiff import OpenApiSpecDiff

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')

class CloudvectorDAST(object):
    def __init__(self, APISpecOne, APISpecTwo, ce_host, ce_username, ce_password, cover_only_diff=False,
                 input_params_file=None):
        self.apispec_one_path = APISpecOne
        self.apispec_two_path = APISpecTwo
        self.ceobj = CommunityEdition.CommunityEdition("http://" + ce_host, ce_username, ce_password)
        print("\n\t\t\t\t\t\t\t\t\t----------------- DAST - For CloudVector APIShark events "
              "-----------------")
        # self.regenerate_traffic(self._get_changed_apis())
        self.input_json = {}
        if not os.path.exists("tests"):
            os.mkdir("tests")

        self.input_json = {}

        for file in input_params_file.split(";"):
            print("loading variables from input file "+str(file)+" .....")
            input_json = {}
            if os.path.exists(file):
                if ".json" in file:
                    with open(file) as fobj:
                        input_json = json.load(fobj)
                else:
                    input_json = self._load_input_from_files(file)
            self.input_json.update(input_json)

        self.params_captured_in_traffic = {}
        changed_apis = self._get_changed_apis()
        apis_to_check = changed_apis["changed"]
        apis_to_check.update(changed_apis["new"])

        cv_events = self._process_event_data(apis_to_check)
        self._process_input_json()

        if cover_only_diff == "y":
            self._process_param_diff(apis_to_check, True)
        else:
            self._process_param_diff(apis_to_check, False)
        with open("tests/params_captured.json", "w+") as fobj:
            json.dump(self.params_captured_in_traffic, fobj)
        self.create_pyfixtures()
        #self.create_fuzzfixtures()
        self.create_pytest_methods(cv_events)

    def _load_input_from_files(self, input_file):
        input_vars = {}
        content = []
        if os.path.exists(input_file):
            with open(input_file) as fobj:
                content = fobj.readlines()
        for each in content:
            if "=" in each:
                key, value = each.split("=")
                if "[" in value and "]" in value:
                    value = eval(value)
                else:
                    value = [value]
                input_vars[str(key).strip()] = value
        return input_vars

    def _scan_input_spec(self, input_path):
        if os.path.isdir(input_path):
            input_spec = {}
            for (root, dirs, files) in os.walk(input_path, topdown=True):
                for file in files:
                    if ".json" in file:
                        print("Parsing the SPEC file: " + str(file))
                        try:
                            with open(os.path.join(root, file)) as specobj:
                                input = json.loads(specobj.read())
                                if "swagger" not in input:
                                    continue
                                if not input_spec:
                                    input_spec = input
                                else:
                                    input_spec["paths"].update(input.get("paths"))
                        except:
                            print("ignoring the SPEC " + str(file) + " due to unforseen exception")
        else:
            with open(input_path) as specobj:
                input_spec = json.loads(specobj.read())
        print(input_spec)
        params_info = {}
        for api, info in input_spec["paths"].items():
            if api not in params_info:
                params_info[api] = {}
            params = []
            for method, paraminfo in info.items():
                for each in paraminfo.get("parameters", []):
                    params.append(each.get("name"))
            params_info[api] = params
        return params_info

    def _get_changed_apis(self):
        return OpenApiSpecDiff.OpenApiSpecDiff(self.apispec_one_path, self.apispec_two_path).diff

    def _process_input_json(self):
        for key, value in self.input_json.items():
            if type(value) is list:
                if "others" not in self.params_captured_in_traffic:
                    self.params_captured_in_traffic["others"] = {}
                self.params_captured_in_traffic["others"].update({key: value})
            elif type(value) is dict:
                for name, values in value.items():
                    if "null" in values:
                        values.remove("null")
                    if key in self.params_captured_in_traffic:
                        self.params_captured_in_traffic[key].update({name: values})

    def _process_param_diff(self, changed_apis, only_diff):
        print(self.params_captured_in_traffic)
        print("\n\n\n")
        if only_diff:
            self.params_captured_in_traffic = {}
        for api, info in changed_apis.items():
            if only_diff:
                self.params_captured_in_traffic[api] = {}
            for method, params in info.items():
                for param in params:
                    if param.get("name") not in self.params_captured_in_traffic[api]:
                        self.params_captured_in_traffic[api].update({param.get("name"): []})

        for api, info in self.params_captured_in_traffic.items():
            for param, value in info.items():
                if param in self.input_json:
                    self.params_captured_in_traffic[api][param] = self.input_json[param]
                if api in self.input_json:
                    if param in self.input_json[api]:
                        self.params_captured_in_traffic[api][param] = self.input_json[api][param]

    def create_pyfixtures(self):
        print("\n\ncreating Pytest fixtures....\n")
        with open(os.path.join(templates_dir,'conftest.j2')) as file_:
            template = Template(file_.read())
        code = template.render(api_info=self.params_captured_in_traffic)
        print(self.validate_pycode_for_syntax(code))
        if not os.path.exists("tests"):
            os.mkdir("tests")
        with open("tests/conftest.py", 'w+') as fh:
            fh.write(template.render(api_info=self.params_captured_in_traffic))
        print("\n\t\t......done creating pytest fixtures (conftest.py)")

    def create_fuzzfixtures(self):
        print("\n\ncreating fuzz-lightyear fixtures....\n")
        with open(os.path.join(templates_dir,'fuzz_fixtures.j2')) as file_:
            template = Template(file_.read())
        code = template.render(api_info=self.params_captured_in_traffic)
        print(self.validate_pycode_for_syntax(code))
        if not os.path.exists("tests"):
            os.mkdir("tests")
        with open("tests/fuzz_fixtures.py", 'w+') as fh:
            fh.write(template.render(api_info=self.params_captured_in_traffic))
        print("\n\t\t......done creating fuzz-lightyear fixtures (fuzz_fixtures.py)")

    def create_pytest_methods(self, cv_events):
        apis_to_be_tested = {}
        files_created = set()
        print("\n\ncreating Pytest test methods....\n")
        new_spec_info = self._scan_input_spec(self.apispec_two_path)
        for _ in cv_events:
            event = _[0]
            if _[1]["attributes"]["http_rsp_status_code"] not in ["200", "201"]:
                continue
            if event["url"] not in apis_to_be_tested:
                api = str(event["http-req-url"]).lstrip("/").rstrip("/").replace("/", "_").replace("-", "_").split("?")[
                    0]
                apis_to_be_tested[api] = {}
                apis_to_be_tested[api]["method"] = event["method"]
                apis_to_be_tested[api]["header"] = event["header"]
                apis_to_be_tested[api]["url"] = event["url"]
                apis_to_be_tested[api]["params"] = new_spec_info.get(str(event["http-req-url"]).replace("//", "/"))
                if apis_to_be_tested[api]["params"] is None:
                    apis_to_be_tested[api]["params"] = []
                host_url = str(event["host"]).lower()
        with open(os.path.join(templates_dir,'test_api.j2')) as file_:
            template = Template(file_.read())
        for k, v in apis_to_be_tested.items():
            # code = template.render(api_info=apis_to_be_tested[k], api_name=k, host_url=host_url)
            filename = str(k).replace("/", "_")
            if not os.path.exists("tests"):
                os.mkdir("tests")

            with open("tests/test_" + str(filename) + ".py", 'w+') as fh:
                fh.write(template.render(api_info=apis_to_be_tested[k], api_name=k, host_url=host_url))
            files_created.add("test_" + str(filename))
        print("\n\t\t......done creating pytest methods: " + str(files_created))

    def get_captured_events(self):
        return self.ceobj.get_all_raw_events()  # last 3 weeks data

    # def _get_changed_apis(self):
    #     return OpenApiSpecDiff.OpenApiSpecDiff(self.apispec_one_path, self.apispec_two_path).diff

    def validate_pycode_for_syntax(self, code):
        code = str(code).replace(" ", "%20").replace("\n", "%0")
        headers = {
            'authority': 'extendsclass.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.129 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://extendsclass.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://extendsclass.com/python-tester.html',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '__gads=ID=da612839d6fc1303:T=1590622404:S=ALNI_MaEgA77keI5Spn5CckEF15zogbT6A; '
                      'PHPSESSID=123dabd5a795c756d1a5f45837f3217d; SERVERID100401=15211|Xs75G|Xs74y',
        }

        data = {
            '$source': code
        }
        print(data)
        response = requests.post('https://extendsclass.com/python-tester-source', headers=headers, data=data)
        print(response.text)
        return response.json()

    def _process_event_data(self, apis_to_check=[]):
        print("\n\ncollecting events data from APIShark....")
        cv_requests = []
        events = self.ceobj.get_all_raw_events(apis_to_check)

        for event in events:
            # if "ce-api" in str(event["attributes"]["http_path"]) or "/platform/api" in str(event["attributes"][
            # "http_path"]): continue print("....."+str(event)) print(event["attributes"]["http_path"])
            if apis_to_check:
                iflag = False
                # params_to_add = []
                for _ in apis_to_check:
                    if str(_).lower() in str(event["attributes"]["http_path"]).lower():
                        iflag = True
                        params_to_add = apis_to_check[_]
                    if iflag:
                        break

                if not iflag:
                    continue

            request = {"url": str(event["attributes"]["event_protocol"]).lower() + "://" + \
                              str(event["attributes"]["http_host"]) + \
                              str(event["attributes"]["http_path"]), "method": str(event["attributes"]["http_method"])}
            header = {}
            body = {}
            params_found = {}
            for k, v in event["attributes"]["event_json"].items():
                if "http-req-header" in k:
                    if k == "http-req-headers-params":
                        continue
                    header[str(k).replace("http-req-header-", "")] = v
                if k in ["http-req-body-params", "http-req-query-params"]:
                    if v:
                        for param in v:
                            params_found[param] = {}

            for param in params_found:
                if "http-req-body-" + str(param) in event["attributes"]["event_json"]:
                    params_found[param] = event["attributes"]["event_json"]["http-req-body-" + str(param)]
                elif "http-req-query-" + str(param) in event["attributes"]["event_json"]:
                    params_found[param] = event["attributes"]["event_json"]["http-req-query-" + str(param)]

            request["host"] = event["attributes"]["event_json"]["http-req-host"]
            request["http-req-url"] = event["attributes"]["event_json"]["http-req-url"]
            request["header"] = header
            request["body"] = params_found
            # if not to_skip:
            # print(event)
            if str(event["attributes"]["http_path"]).lower() not in self.params_captured_in_traffic:
                self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()] = {}
            # print("????"+str(params_found))
            # print(self.params_captured_in_traffic)
            # print("\n\n\n\n\n\n\n")
            for param, value in params_found.items():
                # if "severity" in param:
                #     print(str(event) + "\n\n")
                if param in self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()]:
                    # self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()] = {}
                    if value not in self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()][
                        param]:
                        self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()][param].append(
                            value)
                else:
                    self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()][param] = [value]
            cv_requests.append([request, event])
        print("\n\t\t......done collecting events data from APIShark")
        return cv_requests


def main():
    import sys
    import getpass
    import yaml
    if os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml")) as fobj:
            ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
    else:
        ce_details = {}
    print("\n\n" + "\t" * 8 + "*****" * 20)
    print ("\t" * 11 + "CloudVector - Dynamic Application Security Testing")
    print("\t" * 8 + "*****" * 20)
    print("\nAPIShark details from my_cesetup.yaml:\n\t" + str(ce_details) + "\n")
    if ce_details.get("ce_host"):
        ce_host = ce_details["ce_host"]
    else:
        ce_host = input("Enter APIShark host in format <host>:<port> : ")
    if ce_details.get("ce_username"):
        ce_username = ce_details["ce_username"]
    else:
        ce_username = input("Enter your APIShark username : ")
    ce_password = getpass.getpass(prompt="APIShark password:")
    input_spec_one = input("Enter absolute path to Old API SPEC(Version A): ")
    input_spec_two = input("Enter absolute path to New API SPEC(Version B) : ")
    cover_only_diff = input("Do you want to process only the missing parameters? (Y/N) : ")
    input_params_file = input("Enter absolute path to input parameters file(press Enter for None):")
    if not os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml"), "w+") as fobj:
            yaml.dump({"ce_host": str(ce_host), "ce_username": str(ce_username)}, fobj)
    CloudvectorDAST(input_spec_one, input_spec_two, ce_host, ce_username, ce_password, str(cover_only_diff).lower(),
                    input_params_file)


if __name__ == "__main__":
    main()
