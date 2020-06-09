import json

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.traces import DroppedSpan
from stackifyapm.traces import execution_context
from stackifyapm.utils import default_ports
from stackifyapm.utils.compat import urlparse
from stackifyapm.utils.compat import iteritems
from stackifyapm.utils.helper import is_async_span
from stackifyapm.utils.helper import safe_bytes_to_string


def get_host_from_url(url):
    parsed_url = urlparse.urlparse(url)
    host = parsed_url.hostname or " "

    if parsed_url.port and default_ports.get(parsed_url.scheme) != parsed_url.port:
        host += ":" + str(parsed_url.port)

    return host


class RequestsInstrumentation(AbstractInstrumentedModule):
    name = "requests"

    instrument_list = [("requests.sessions", "Session.send")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        if "request" in kwargs:
            request = kwargs["request"]
        else:
            request = args[0]

        extra_data = {
            "wrapped_method": "Execute",
            "provider": self.name,
            "type": "Web External",
            "sub_type": "send",
            "request_method": request.method,
            "url": request.url,
        }

        with CaptureSpan("ext.http.requests", extra_data, leaf=True, is_async=is_async_span()) as span:
            response = wrapped(*args, **kwargs)

            if not isinstance(span, DroppedSpan):
                span.context['status_code'] = response.status_code

                if self.client and self.client.config.prefix_enabled:
                    request_body = safe_bytes_to_string(request.body)
                    response_body = safe_bytes_to_string(response.content)
                    span.context['request_body'] = request_body
                    span.context['request_body_size'] = len(request_body)
                    span.context['request_headers'] = json.dumps([{key: value} for key, value in iteritems(request.headers)])
                    span.context['response_body'] = response_body
                    span.context['response_body_size'] = len(response_body)
                    span.context['response_headers'] = json.dumps([{key: value} for key, value in iteritems(response.headers)])

                transaction = execution_context.get_transaction()
                transaction.update_span_context(span.id, span.context)

            return response
