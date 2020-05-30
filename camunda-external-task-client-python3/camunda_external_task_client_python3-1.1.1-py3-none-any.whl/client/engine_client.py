import logging
from http import HTTPStatus

from aiohttp_requests import requests as req

from camunda.variables.variables import Variables

logger = logging.getLogger(__name__)

ENGINE_LOCAL_BASE_URL = "http://localhost:8080/engine-rest"


class EngineClient:

    def __init__(self, engine_base_url=ENGINE_LOCAL_BASE_URL):
        self.engine_base_url = engine_base_url

    def get_start_process_instance_url(self, process_key, tenant_id=None):
        if tenant_id:
            return f"{self.engine_base_url}/process-definition/key/{process_key}/tenant-id/{tenant_id}/start"
        return f"{self.engine_base_url}/process-definition/key/{process_key}/start"

    async def start_process(self, process_key, variables, tenant_id=None):
        url = self.get_start_process_instance_url(process_key, tenant_id)
        body = {
            "variables": Variables.format(variables)
        }

        response = await req.post(url, headers=self._get_headers(), json=body)
        resp_json = await response.json()
        if response.status == HTTPStatus.OK:
            return resp_json
        elif response.status == HTTPStatus.NOT_FOUND or response.status == HTTPStatus.BAD_REQUEST:
            raise Exception(resp_json["message"])
        else:
            response.raise_for_status()

    async def get_process_instance(self, process_key=None, variables=frozenset([]), tenant_ids=frozenset([])):
        url = f"{self.engine_base_url}/process-instance"
        url_params = self.__get_process_instance_url_params(process_key, tenant_ids, variables)
        response = await req.get(url, headers=self._get_headers(), params=url_params)
        resp_json = await response.json()
        if response.status == HTTPStatus.OK:
            return resp_json
        elif response.status == HTTPStatus.BAD_REQUEST:
            raise Exception(resp_json["message"])
        else:
            response.raise_for_status()

    def __get_process_instance_url_params(self, process_key, tenant_ids, variables):
        url_params = {}
        if process_key:
            url_params["processDefinitionKey"] = process_key
        var_filter = self.join(variables, ',')
        if var_filter:
            url_params["variables"] = var_filter
        tenant_ids_filter = self.join(tenant_ids, ',')
        if tenant_ids_filter:
            url_params["tenantIdIn"] = tenant_ids_filter
        return url_params

    def _get_headers(self):
        return {
            "Content-Type": "application/json"
        }

    def join(self, list_of_values, separator):
        return separator.join(str(v) for v in list_of_values)
