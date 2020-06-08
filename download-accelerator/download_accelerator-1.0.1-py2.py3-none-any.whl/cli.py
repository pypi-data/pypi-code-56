"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mdownload_accelerator` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``download_accelerator.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``download_accelerator.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import asyncio

import argh

from .file_tools import write_to_file
from .network_tools import parallel_download


def download(link: str, output: str = "", connections: int = 32, return_bytes: bool = False,
             disable_progress_bar: bool = False):
    """
    Download a link using parallel multiple connections
    Args:
        link: a link to download.
        output: Output to save your link to. if you set return_bytes=True then this output will be ignored.
        connections: number of parallel connections that is used to download your link.
        return_bytes: if true the method will return the bytes other than writing them to output
        disable_progress_bar: if true. the program won't show a progress bar.
    Returns: if return_bytes will return all the bytes downloaded.

    """
    loop = asyncio.get_event_loop()
    try:
        content: bytes = loop.run_until_complete(parallel_download(link, connections, disable_progress_bar))
        if return_bytes:
            return content
        write_to_file(output, content, "downloaded files")
        return None
    finally:
        loop.close()


parser = argh.ArghParser()
parser.add_commands([download])

# dispatching:

if __name__ == '__main__':
    parser.dispatch()
