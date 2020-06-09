import json

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.traces import DroppedSpan
from stackifyapm.traces import execution_context
from stackifyapm.utils import default_ports
from stackifyapm.utils.compat import iteritems
from stackifyapm.utils.helper import is_async_span
from stackifyapm.utils.helper import safe_bytes_to_string


class Urllib3Instrumentation(AbstractInstrumentedModule):
    name = "urllib3"

    instrument_list = [
        ("urllib3.connectionpool", "HTTPConnectionPool.urlopen"),
        ("requests.packages.urllib3.connectionpool", "HTTPConnectionPool.urlopen"),
    ]

    def call(self, module, method, wrapped, instance, args, kwargs):
        if "method" in kwargs:
            request_method = kwargs["method"]
        else:
            request_method = args[0]

        host = instance.host

        if instance.port != default_ports.get(instance.scheme):
            host += ":" + str(instance.port)

        if "url" in kwargs:
            url = kwargs["url"]
        else:
            url = args[1]

        url = instance.scheme + "://" + host + url
        extra_data = {
            "wrapped_method": "Execute",
            "provider": self.name,
            "type": "Web External",
            "sub_type": "send",
            "url": url,
            "request_method": request_method.upper(),
        }

        with CaptureSpan("ext.http.urllib3", extra_data, leaf=True, is_async=is_async_span()) as span:
            leaf_span = span
            while isinstance(leaf_span, DroppedSpan):
                leaf_span = leaf_span.parent

            response = wrapped(*args, **kwargs)
            if not isinstance(span, DroppedSpan):
                span.context['status_code'] = response.status

                if self.client and self.client.config.prefix_enabled:
                    request_body = safe_bytes_to_string(kwargs.get('body', ''))
                    response_body = safe_bytes_to_string(response.data)

                    span.context['request_body'] = request_body
                    span.context['request_body_size'] = str(len(request_body))
                    span.context['request_headers'] = json.dumps([{key: value} for key, value in iteritems(kwargs.get('headers', {}))])
                    span.context['response_body'] = response_body
                    span.context['response_body_size'] = str(len(response_body))
                    span.context['response_headers'] = json.dumps([{key: value} for key, value in iteritems(response.headers)])

                transaction = execution_context.get_transaction()
                transaction.update_span_context(span.id, span.context)

            return response
