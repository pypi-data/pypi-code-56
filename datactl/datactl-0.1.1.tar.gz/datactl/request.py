import threading
import urllib.parse as urlparse
from urllib.parse import urlencode

from termcolor import colored, cprint

from datactl.utils import abort, confirm, dry_run, prepare_data

POST, GET, DELETE = 'POST', 'GET', 'DELETE'


def add_params_to_url(obj, msg, param):
    url = obj._url
    if param:
        url = url.format(**param)
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(msg)
    url_parts[4] = urlencode(query)
    url = urlparse.urlunparse(url_parts)
    if obj._verbose:
        cprint(colored('url: {}'.format(url), color='cyan'))
    return url


class Request():

    def __init__(self, obj):
        self._obj = obj

    def _get_client(self, force=False):
        cprint('url=<%s>' % self._obj._url)
        cprint('workers=<%s>' % self._obj._workers)
        cprint('size=%s timeout=%s seconds' %
               (self._obj._size, self._obj._timeout))
        if not force and not confirm(self._obj):
            abort()
        import requests
        app = requests
        if self._obj._timeout:
            app.ConnectTimeout = self._obj._timeout
        return app

    def _request(self, r, name, method, msgs, params, results):
        results.setdefault(name, {})
        for msg, param in zip(msgs, params):
            try:
                if method == POST:
                    res = r.request(
                        method=method, url=add_params_to_url(self._obj, msg, param), data=msg)
                elif method == GET:
                    res = r.request(
                        method=method, url=add_params_to_url(self._obj, msg, param), data=msg)
                elif method == DELETE:
                    res = r.request(
                        method=method, url=add_params_to_url(self._obj, msg, param), data=msg)
                results[name].setdefault(res.status_code, 0)
                results[name][res.status_code] += 1
                if self._obj._verbose:
                    results[name].setdefault('results', [])
                    try:
                        results[name]['results'].append(eval(res.content)) #pylint: disable=eval-used
                    except:
                        results[name]['results'].append(res.content)
            except Exception as e: #pylint: disable=broad-except
                results[name].setdefault('failed', 0)
                results[name]['failed'] += 1
                print(e)

    def _send_request(self, method, msg, param, size):
        results = {}
        self._obj._size = abs(size if size is not None else self._obj._size)
        msgs = prepare_data(str(msg), self._obj)
        params = prepare_data(str(param), self._obj)
        dry_run(msgs, self._obj)
        r = self._get_client()
        threads = []
        for w in range(self._obj._workers):
            t = threading.Thread(target=self._request, args=(
                r, f'worker {w+1}', method, msgs, params, results))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        for worker, status in results.items():
            status_str = ' '.join([
                '{}={}'.format(k, v) for k, v in status.items()
            ])
            cprint(colored('{} - count: {}'.format(worker, status_str), color='green'))

    def post(self, query="", param="", size=None):
        '''
        post json data
        '''
        self._send_request(POST, query, param, size)

    def get(self, query="", param="", size=None):
        '''
        get some data
        '''
        self._send_request(GET, query, param, size)

    def delete(self, query="", param="", size=None):
        '''
        delete some data
        '''
        self._send_request(DELETE, query, param, size)
