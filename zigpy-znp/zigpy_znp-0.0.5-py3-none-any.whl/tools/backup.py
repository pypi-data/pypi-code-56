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


async def backup(radio_path):
    znp = ZNP(CONFIG_SCHEMA({"device": {"path": radio_path}}))

    await znp.connect()

    data = {
        "osal": {},
        "nwk": {},
    }

    for nwk_nvid in NwkNvIds:
        try:
            value = await znp.nvram_read(nwk_nvid)
            LOGGER.info("%s = %s", nwk_nvid, value)

            data["nwk"][nwk_nvid.name] = value.hex()
        except InvalidCommandResponse:
            LOGGER.warning("Read failed for %s", nwk_nvid)
            continue

    for osal_nvid in OsalExNvIds:
        length_rsp = await znp.request(
            c.SYS.NVLength.Req(SysId=1, ItemId=osal_nvid, SubId=0)
        )
        length = length_rsp.Length

        if length == 0:
            LOGGER.warning("Read failed for %s", osal_nvid)
            continue

        value = (
            await znp.request(
                c.SYS.NVRead.Req(
                    SysId=1, ItemId=osal_nvid, SubId=0, Offset=0, Length=length
                ),
                RspStatus=t.Status.SUCCESS,
            )
        ).Value
        LOGGER.info("%s = %s", osal_nvid, value)

        data["osal"][osal_nvid.name] = value.hex()

    return data


async def main(argv):
    parser = argparse.ArgumentParser(description="Backup a radio's NVRAM")
    parser.add_argument("serial", type=argparse.FileType("rb"), help="Serial port path")
    parser.add_argument(
        "--output", "-o", type=argparse.FileType("w"), help="Output file", default="-"
    )

    args = parser.parse_args(argv)

    # We just want to make sure it exists
    args.serial.close()

    obj = await backup(args.serial.name)

    args.output.write(json.dumps(obj, indent=4))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
