from scrapy.http import TextResponse

from shangyun_scrapy_lib.utils.response import JsonResponse


class JSONPathDownloaderMiddleware(object):
    def process_response(self, request, response: TextResponse, spider):
        if "application/json;charset=UTF-8" in response.headers.to_unicode_dict().get("Content-Type"):
            return JsonResponse.copy_from(response)
        return response