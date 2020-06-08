import asyncio
import logging
from asyncio.futures import Future
from typing import Any, Union, Set, Optional

from google.protobuf import message as _message

from .channels.websocket_client import AbstractMsgHandler
from .channels.websocket_client import ubt_websocket as _websocket
from .dns.dns_browser import WiFiDeviceListener, WiFiDevice
from .dns.dns_browser import browser as _browser

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
if log.level == logging.NOTSET:
    log.setLevel(logging.INFO)

browser = _browser()
websocket = _websocket()

"""
批量获取机器人设备监听类
"""


def set_log_level(level: int, save_file: str = None):
    log.setLevel(level)

    from .dns.dns_browser import log as log1
    log1.setLevel(log.level)

    from .channels.websocket_client import log as log2
    log2.setLevel(log.level)

    if save_file is not None:
        file_handler = logging.FileHandler(save_file)
        log.addHandler(file_handler)
        log1.addHandler(file_handler)
        log2.addHandler(file_handler)


class GetWiFiDeviceListListener(WiFiDeviceListener):
    devices: Union[Set[Any], Any]

    def __init__(self, devices):
        self.devices = devices or set()

    def on_device_updated(self, device: WiFiDevice) -> None:
        pass

    def on_device_removed(self, device: WiFiDevice) -> None:
        self.devices.remove(device)

    def on_device_found(self, device: WiFiDevice) -> None:
        self.devices.add(device)


"""
获取用户选择的机器人序号
"""


async def get_user_input(devices: tuple) -> int:
    try:
        i: int = 0
        for device in devices:
            print('{0}.{1}'.format(i, device))
            i += 1
        num_text = input(f'请输入选择连接的机器人序号:')
    except Exception as e:
        raise e
    else:
        return int(num_text)


"""
开启一个扫描机器人设备的任务
"""


def start_scan(loop: asyncio.AbstractEventLoop, name: str) -> Future:
    fut = loop.create_future()

    class _InnerLister(WiFiDeviceListener):

        @staticmethod
        def set_result(future: Future, device: WiFiDevice):
            if future.cancelled() or future.done():
                return
            log.info(f"found device : {device}")
            future.set_result(device)

        def on_device_found(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.run_in_executor(None, browser.stop_scan)
                loop.call_soon(_InnerLister.set_result, fut, device)

        def on_device_updated(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.run_in_executor(None, browser.stop_scan)
                loop.call_soon(_InnerLister.set_result, fut, device)

        def on_device_removed(self, device: WiFiDevice) -> None:
            if device.name.endswith(name):
                if fut.cancelled() or fut.done():
                    return
                loop.call_soon(_InnerLister.set_result, fut, device)

    log.info("start scanning...")
    browser.add_listener(_InnerLister())
    browser.start_scan(0)

    return fut


"""
获取当前局域网内，指定名字的机器人设备信息
"""


async def get_device_by_name(name: str, timeout: int) -> Optional[WiFiDevice]:
    async def start_scan_async():
        return await start_scan(asyncio.get_running_loop(), name)

    try:
        device: WiFiDevice = await asyncio.wait_for(start_scan_async(), timeout)
        return device
    except asyncio.TimeoutError:
        log.warning(f'scan device timeout')
        return None
    finally:
        browser.stop_scan()
        log.info("stop scan finished.")


"""
获取当前局域网内所有机器人设备信息
"""


async def get_device_list(timeout: int):
    devices: Set[WiFiDevice] = set()
    browser.add_listener(GetWiFiDeviceListListener(devices))
    browser.start_scan(0)
    await asyncio.sleep(timeout)
    browser.remove_all_listener()
    browser.stop_scan()
    return tuple(devices)


"""
链接机器人设备
"""


async def connect(device: WiFiDevice) -> bool:
    return await websocket.connect(device.address)


"""
注册命令监听器
"""


def register_msg_handler(cmd: int, handler: AbstractMsgHandler):
    websocket.register_msg_handler(cmd, handler)


"""
反注册命令监听器
"""


def unregister_msg_handler(cmd: int, handler: AbstractMsgHandler):
    websocket.unregister_msg_handler(cmd, handler)


"""
发送一个消息给机器人
"""


async def send_msg(cmd: int, message: _message.Message, timeout: int) -> Any:
    return await websocket.send_msg(cmd, message, timeout)


"""
断开链接，释放资源
"""


async def release():
    await websocket.shutdown()
