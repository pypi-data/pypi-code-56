import json

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.traces import DroppedSpan
from stackifyapm.traces import execution_context
from stackifyapm.utils.helper import is_async_span
from stackifyapm.utils.helper import safe_bytes_to_string


class UrllibInstrumentation(AbstractInstrumentedModule):
    name = "urllib"

    instrument_list = [
        ("urllib", "URLopener.open"),
        ("urllib.request", "AbstractHTTPHandler.do_open"),
    ]

    def call(self, module, method, wrapped, instance, args, kwargs):
        if method == "URLopener.open":
            url = args[0]
            request_method = len(args) > 1 and 'POST' or 'GET'
        else:
            request_object = args[1] if len(args) > 1 else kwargs["req"]
            request_method = request_object.get_method()
            url = request_object.get_full_url()

        extra_data = {
            "wrapped_method": "Execute",
            "provider": self.name,
            "type": "Web External",
            "sub_type": "send",
            "url": url,
            "request_method": request_method,
        }

        with CaptureSpan("ext.http.urllib", extra_data, leaf=True, is_async=is_async_span()) as span:
            response = wrapped(*args, **kwargs)

            if not isinstance(span, DroppedSpan):
                span.context['status_code'] = response.code

                if self.client and self.client.config.prefix_enabled:
                    if method == "URLopener.open":
                        request_body = safe_bytes_to_string(len(args) > 1 and args[1] or "")
                        request_headers = json.dumps([{key: value} for key, value in instance.addheaders])
                    else:
                        request_body = safe_bytes_to_string(request_object.data)
                        request_headers = json.dumps([{key: value} for key, value in request_object.header_items()])

                    response_body = ""  # unable to get response context coz it will alter the return data cStringIO.StringO
                    response_headers = json.dumps([{key: value} for key, value in response.headers.items()])

                    span.context['request_body'] = request_body
                    span.context['request_body_size'] = len(request_body)
                    span.context['request_headers'] = request_headers
                    span.context['response_body'] = response_body
                    span.context['response_body_size'] = len(response_body)
                    span.context['response_headers'] = response_headers

                transaction = execution_context.get_transaction()
                transaction.update_span_context(span.id, span.context)

            return response
