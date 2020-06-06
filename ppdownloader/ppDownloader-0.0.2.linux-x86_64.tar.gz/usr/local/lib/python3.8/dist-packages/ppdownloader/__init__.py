__version__ = '0.0.2'

import asyncio

import argh
from ppdownloader.parallel_download import parallel_download, write_to_file

DISPLAY_PROGRESS: bool = True
DISPLAY_STARTUP: bool = True


async def _download(link: str, output: str, connections: int = 32, return_bytes: bool = False,
                    disable_progress_bar=True):
    """
    downloads the content and writes them to a file.
    :param link: this method will download this link from the internet.
    :param output: it will write the downloaded content from link to this output.
    :param connections: number of connections that we are allowed to use for this purpose.
    :return:
    """
    content: bytes = await parallel_download(link, connections, disable_progress_bar)
    if return_bytes:
        return content
    write_to_file(output, content, "downloaded files")


def download(link: str, output: str = "", connections: int = 32, return_bytes: bool = False,
             disable_progress_bar: bool = False) -> bytes:
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
        return loop.run_until_complete(_download(link, output, connections, return_bytes, disable_progress_bar))
    finally:
        loop.close()
