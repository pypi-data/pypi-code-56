import sys
import json
import asyncio
import logging
import argparse
import coloredlogs

import zigpy_znp.types as t
import zigpy_znp.commands as c

from zigpy_znp.api import ZNP
from zigpy_znp.config import CONFIG_SCHEMA
from zigpy_znp.exceptions import InvalidCommandResponse
from zigpy_znp.types.nvids import NwkNvIds, OsalExNvIds

coloredlogs.install(level=logging.DEBUG)
logging.getLogger("zigpy_znp").setLevel(logging.DEBUG)

LOGGER = logging.getLogger(__name__)


async def restore(radio_path, backup):
    znp = ZNP(CONFIG_SCHEMA({"device": {"path": radio_path}}))

    await znp.connect()

    for nwk_nvid, value in backup["nwk"].items():
        nvid = NwkNvIds[nwk_nvid]
        value = bytes.fromhex(value)

        # XXX: are any NVIDs not filled all the way?
        init_rsp = await znp.request(
            c.SYS.OSALNVItemInit.Req(Id=nvid, ItemLen=len(value), Value=value)
        )
        assert init_rsp.Status in (t.Status.SUCCESS, t.Status.NV_ITEM_UNINIT)

        try:
            await znp.nvram_write(nvid, value)
        except InvalidCommandResponse:
            LOGGER.warning("Write failed for %s = %s", nvid, value)

    for osal_nvid, value in backup["osal"].items():
        nvid = OsalExNvIds[osal_nvid]
        value = bytes.fromhex(value)

        try:
            await znp.request(
                c.SYS.NVWrite.Req(SysId=1, ItemId=nvid, SubId=0, Offset=0, Value=value),
                RspStatus=t.Status.SUCCESS,
            )
        except InvalidCommandResponse:
            LOGGER.warning("Write failed for %s = %s", nvid, value)

    # Reset afterwards to have the new values take effect
    await znp.request_callback_rsp(
        request=c.SYS.ResetReq.Req(Type=t.ResetType.Soft),
        callback=c.SYS.ResetInd.Callback(partial=True),
    )


async def main(argv):
    parser = argparse.ArgumentParser(
        description="Restore a radio's NVRAM from a previous backup"
    )
    parser.add_argument("serial", type=argparse.FileType("rb"), help="Serial port path")
    parser.add_argument(
        "--input", "-i", type=argparse.FileType("r"), help="Input file", required=True
    )

    args = parser.parse_args(argv)

    # We just want to make sure it exists
    args.serial.close()

    backup = json.load(args.input)
    await restore(args.serial.name, backup)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
