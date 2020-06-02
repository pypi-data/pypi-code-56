import json
import logging
import os
import requests

DEFAULT_REGION = "northeurope"


class AzureBase:
    """Library for interacting with Azure services

    Requires environment variable `AZURE_SUBSCRIPTION_KEY`
    to use.

    https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
    """

    COGNITIVE_API = "api.cognitive.microsoft.com"
    services = {}

    def __init__(self, region="northeurope"):
        self.region = region
        self.services = {}

    def _azure_post(self, service_name, url, params=None, filepath=None, jsondata=None):
        if service_name not in self.services or self.services[service_name] is None:
            raise KeyError("Missing subscription key for service: %s" % service_name)
        self.logger.info(self.services[service_name])
        request_parameters = {"headers": {}}
        request_parameters["headers"]["Ocp-Apim-Subscription-Key"] = self.services[
            service_name
        ]
        request_parameters["headers"]["Content-Type"] = "application/json"
        if filepath:
            request_parameters["headers"]["Content-Type"] = "application/octet-stream"
            with open(filepath, "rb") as f:
                filedata = f.read()
            request_parameters["data"] = filedata
        elif jsondata:
            request_parameters["json"] = jsondata
        if params:
            request_parameters["params"] = params
        self.logger.debug("Azure POST: %s" % url)
        self.logger.debug(
            "Content-Type: %s" % request_parameters["headers"]["Content-Type"]
        )
        response = requests.post(url, **request_parameters)
        return response

    def _write_json(self, json_file, response):
        if json_file and response:
            with open(json_file, "w") as f:
                json.dump(response.json(), f)

    def _set_subscription_key(self, service_name):
        sub_key = os.getenv(f"AZURE_{service_name.upper()}_KEY")
        self.services[service_name] = sub_key


class ServiceTextAnalytics(AzureBase):
    """Class for Azure TextAnalytics service"""

    __service_name = "textanalytics"

    def __init__(self) -> None:
        self.logger.debug("ServiceTextAnalytics init")

    def init_textanalytics_service(self, region: str = None):
        self.__region = region if region else self.region
        self.__base_url = f"https://{self.__region}.{self.COGNITIVE_API}"
        self._set_subscription_key(self.__service_name)

    def vision_analyze(self, image_file: str, json_file: str = None):
        analyze_url = f"{self.__base_url}/vision/v3.0/analyze"
        params = {"visualFeatures": "Categories,Description,Color"}
        response = self._azure_post(
            self.__service_name, analyze_url, params=params, filepath=image_file
        )
        self._write_json(json_file, response)
        return response.json()

    def sentiment_analyze(self, documents, json_file=None):
        analyze_url = f"{self.__base_url}/text/analytics/v3.0/sentiment"
        response = self._azure_post(
            self.__service_name, analyze_url, jsondata=documents
        )
        self._write_json(json_file, response)
        return response.json()


class ServiceFace(AzureBase):
    """Class for Azure Text Analytics service"""

    __service_name = "face"

    def __init__(self) -> None:
        self.logger.debug("ServiceFace init")

    def init_face_service(self, region: str = None):
        self.__region = region if region else self.region
        self.__base_url = f"https://{self.__region}.{self.COGNITIVE_API}"
        self._set_subscription_key(self.__service_name)

    def detect_face(self, image_file: str, json_file: str = None):
        analyze_url = f"{self.__base_url}/face/v1.0/detect"
        params = {
            "returnFaceId": "true",
            "returnFaceLandmarks": "false",
            "returnFaceAttributes": "age,gender,smile,facialHair,glasses,emotion,hair",
            "recognitionModel": "recognition_01",
            "returnRecognitionModel": "false",
        }
        response = self._azure_post(
            self.__service_name, analyze_url, params=params, filepath=image_file
        )
        self._write_json(json_file, response)
        return response.json()


class ServiceComputerVision(AzureBase):
    """Class for Azure Computer Vision service"""

    __service_name = "computervision"

    def __init__(self) -> None:
        self.logger.debug("ServiceComputerVision init")

    def init_computervision_service(self, region: str = None):
        self.__region = region if region else self.region
        self.__base_url = f"https://{self.__region}.{self.COGNITIVE_API}"
        self._set_subscription_key(self.__service_name)


class Azure(ServiceTextAnalytics, ServiceFace):
    """Library for interacting with Azure services

    Supported services:

        - TextAnalytics
        - Face
        - SpeechServices
        - Computer Vision
        - Language Understanding (LUIS)

    """

    def __init__(self, region: str = DEFAULT_REGION):
        self.logger = logging.getLogger(__name__)
        ServiceTextAnalytics.__init__(self)
        ServiceFace.__init__(self)
        self.region = region
        self.logger.info("Azure library initialized. Default region: %s" % self.region)
