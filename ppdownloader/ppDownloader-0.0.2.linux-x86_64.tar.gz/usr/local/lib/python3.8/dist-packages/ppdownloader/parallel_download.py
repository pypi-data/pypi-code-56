from typing import Tuple

import aiohttp
import asyncio

import funcy
import tqdm

is_running = True
ENABLE_PARTS_PROGRESS = True


def write_to_file(output: str, content: bytes, name: str, position: int = 0) -> None:
    with open(output, "wb") as file:
        chunks = funcy.chunks(1024, content)
        with tqdm.tqdm(desc=f"Writing {name} to {output}",
                       total=len(content), unit="B", unit_scale=True, unit_divisor=1024,
                       position=position) as bar:
            for chunk in chunks:
                bar.update(len(chunk))
                file.write(chunk)


async def get_content_length(url: str, session: aiohttp.ClientSession) -> int:
    async with session.get(url) as response:
        content_length = int(response.content_length)
    return content_length


async def parallel_download(link: str, connections: int = 32, disable_progress_bar: bool = True) -> bytes:
    async with aiohttp.ClientSession() as session:
        length = await get_content_length(link, session)
        global ENABLE_PARTS_PROGRESS
        ENABLE_PARTS_PROGRESS = not disable_progress_bar
        # Chunkify
        chunks_length = length // connections
        chunks_list = [[i, i + chunks_length - 1] for i in range(0, length, chunks_length)]
        for i, chunk in enumerate(chunks_list):
            if chunk[1] - chunk[0] + 1 < 10:
                removed_chunk = chunks_list.pop(i)
                chunks_list[i - 1][1] = removed_chunk[1]
        chunks_list[-1][-1] = length
        bar = tqdm.tqdm(position=0,
                        desc=f"Downloading",
                        total=length, unit="B", unit_scale=True, unit_divisor=1024)
        bar.write(f"Length {length}")
        tasks = list(
            map(lambda x: parallel_download_range(link, session, x[1], x[0] + 1, parent_bar=bar),
                list(enumerate(chunks_list))))
        contents = []
        for chunk in asyncio.as_completed(tasks):
            content, i = await chunk
            contents.append([i, content])
            bar.update(len(content))
        contents.sort(key=lambda x: x[0])
        contents = list(map(lambda x: x[1], contents))
        downloaded_bytes = b''.join(contents)
        assert len(downloaded_bytes) == length
        return downloaded_bytes


async def parallel_download_range(link: str, session: aiohttp.ClientSession,
                                  link_range: range, i: int, parent_bar=None) -> Tuple[bytes, int]:
    start, stop = list(link_range)[0], list(link_range)[-1]
    content = await _download(link, start, stop, session, i, parent_bar)
    return content, i


async def _download(link: str, start: int, stop: int, session: aiohttp.ClientSession, i: int = 0,
                    parent_bar=None, use_bar: tqdm.std = None) -> bytes:
    """
    This method downloads a file with specific range header.
    :param link: a link to download
    :param start: start in range header
    :param stop: stop in range header
    :param session: aio http session to use for downloading.
    :param i: the position of progress bar.
    :param parent_bar: the parent progress bar to update.
    :param use_bar: if failed method uses the previous progress bar.
    :return:
    """
    parent_bar = tqdm.tqdm(disable=True) if not parent_bar else parent_bar  # if parent bar exists update it
    bar = use_bar
    if use_bar is None:
        bar = tqdm.tqdm(
            desc=f"downloading part {i}", position=i,
            total=stop - start + 1, unit="b",
            unit_scale=True, unit_divisor=1024, leave=True, disable=not ENABLE_PARTS_PROGRESS)
    headers = {"range": str(f"bytes={start}-{stop}")}
    buffer = b""
    try:
        async with session.request("get", link, headers=headers) as response:
            bar.set_postfix(status=str(response.status))
            while response.status not in [206]:
                headers = {"range": str(f"bytes={start}-{stop}")}
                await asyncio.sleep(1)
                response = session.request("get", link, headers=headers)
            async for raw_data in response.content.iter_any():
                bar.set_postfix(status=str(response.status))
                buffer += raw_data
                bar.update(len(raw_data))
                parent_bar.update(len(raw_data))
    except (aiohttp.ClientPayloadError, asyncio.TimeoutError, Exception):
        return buffer + await _download(link, start + len(buffer) + 1, stop, session, i, parent_bar, bar)
    return buffer
