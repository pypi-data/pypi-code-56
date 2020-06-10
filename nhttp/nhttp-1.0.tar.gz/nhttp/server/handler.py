import os
from urllib.parse import quote, unquote

from .req_info import Request
from .resp_writer import ResponseWriter
from ..content_type import content_type_manager


__all__ = ['Handler', 'FuncHandler', 'RedirectHandler', 
           'FileServerHandler', 
           'HelloNezhaHandler', 'HelloWorldHandler']


class Handler:
    def serve_http(self, response_writer :ResponseWriter, request :Request):
        pass


class FuncHandler(Handler):
    def __init__(self, handle_func):
        self.__handle_func = handle_func

    def serve_http(self, response_writer :ResponseWriter, request :Request):
        return self.__handle_func(response_writer, request)


class RedirectHandler(Handler):
    def __init__(self, location :str):
        self.__location = location

    def serve_http(self, w :ResponseWriter, r :Request):
        w.send_respone(301)
        w.send_header({'location': self.__location})



class FileServerHandler(Handler):
    __HTML_TEMPLATE = (
            '<head>'
            '<meta charest = "UTF-8">'
            '<title> dictionary of {title} </title>'
            '</head>'
            '<body>'
            '<h1> dictionary of {dpath} </h1>'
            '<hr/>'
            '{items}'
            '</body>'
        )

    __ITEM_TEMPLATE = '<a href = {tpath}> {item_name} </a>\n'

    def __init__(self, prefix_path :str, real_path :str, view :bool=True):
        self.__prefix_path = prefix_path
        self.__real_path = real_path

        self.__view = view

    def serve_http(self, w :ResponseWriter, r :Request):
        path = r.url

        if path[:len(self.__prefix_path)] != self.__prefix_path:
            raise w.send_error(404, 'File not found')

        cpath = path[len(self.__prefix_path):]
        rpath = os.path.join(self.__real_path, cpath)

        # print('FileServerHandler: \n\trpath: \'%s\'\n\tpath: %s' % 
        #                 (self.__real_path, path))
        
        if not os.path.exists(rpath):
            w.send_error(404, 'File not found')
            return

        if os.path.isdir(rpath):
            if self.__view:
                self.__handle_dir(w, rpath)

            else:  # find index.html
                indp = rpath + '/' + 'index.htm'
                indpl = indp + 'l'  # .html

                target = indpl
                
                if os.path.exists(indpl):
                    pass  # target is indpl

                elif os.path.exists(indp):
                    target = indp

                else:
                    w.send_error(404, 'Not found')
                    return

                self.__handle_file(w, target)

        elif os.path.isfile(rpath):
            self.__handle_file(w, rpath)

        else:
            w.send_error(500, 'Unknown target type')

    def __safe_text(self, text :str) -> str:
        return text.replace(' ', '%20')

    def __get_content_type(self, fpath :str) -> str:
        _, fext = os.path.splitext(fpath)

        return content_type_manager.get(fext) 

    def __handle_dir(self, w :ResponseWriter, rpath :str):
        w.send_respone(200)
        w.send_header({'content-type': 'text/html'})

        html_source = self.__HTML_TEMPLATE.format(
                    title=rpath,  
                    dpath=rpath,
                    items=self.__make_dir_content(rpath),
                ).encode('UTF-8')

        w.write_bytes(html_source)

    def __handle_file(self, w :ResponseWriter, rpath :str):
        w.send_respone(200)
        w.send_header({'content-type': self.__get_content_type(rpath)})
        w.write_bytes(self.__make_file_content(rpath))

    def __make_file_content(self, path :str) -> bytes:
        return open(path, 'rb').read()

    def __make_dir_content(self, path :str) -> str:
        items = {}

        if path[:-1] != self.__real_path:  # [:-1] to remove '/'
            items['..'] = '..'

        d = os.listdir(path)

        for item in d:
            jp = os.path.join(path, item)
            
            if os.path.isdir(jp):
                items['./' + quote(item) + '/'] = os.path.split(item)[-1] + '/'

            elif os.path.isfile(jp):
                items['./' + quote(item)] = os.path.split(item)[-1]

        hitems = [self.__ITEM_TEMPLATE.format(
            tpath=p,
            item_name=n,
            ) for p, n in items.items()]

        return '<br/>'.join(hitems)


class HelloWorldHandler(Handler):
    def serve_http(self, w :ResponseWriter, _):
        w.send_respone(200)
        w.send_header({'content-type': 'text/html'})

        w.write('Hello World!')


class HelloNezhaHandler(Handler):
    def serve_http(self, w :ResponseWriter, _):
        w.send_respone(200)
        w.send_header({'content-type': 'text/html'})

        w.write('Hello Nezha!')
