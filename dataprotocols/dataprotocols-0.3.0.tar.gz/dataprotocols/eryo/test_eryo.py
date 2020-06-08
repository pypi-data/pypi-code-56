from dataprotocols.eryo import Eryo
import asyncio
import functools
import os
import signal
import json
import time
import click
# TEST
#  CHDA,200.9.100.194,12323
# CODE = 'CHDA'
# IP = "200.9.100.194"
# PORT = 12323


async def run_test(loop, code, host, port, limit=2000):
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    eryo = Eryo(**ginput)
    idc = await eryo.connect()
    eryo_test = "eryo_test.json"
    limit_counter = limit
    counter = 0
    with open(eryo_test, "a+") as eryo_file:
        eryo_file.write("[")
        while counter <= limit_counter:
            try:
                eryo.hard_beat(idc)
                await eryo.get_message_header(idc)
                done, msg = await eryo.get_records()
                if done:
                    print("Eryo", msg)
                    json.dump(msg, eryo_file, indent=2)
                    eryo_file.write(",\n")
            except Exception as ex:
                eryo_file.write("]")
                print("Error %s" % ex)
                loop.close()
            except KeyboardInterrupt as ke:
                eryo_file.write("]")
                loop.close()
                print(ke)
            counter += 1
        eryo_file.write("]")

# CODE = 'CHDA'
# IP = "200.9.100.194"
# PORT = 12323

@click.command()
@click.option("--code", default="CHDA", help="Código de estación")
@click.option("--host", default="200.9.100.194", help="URL de estación")
@click.option("--port", default=12323, help="Nro de puerto")
@click.option("--limit", default=2000, help="Nro de mensajes")
def run_eryo(code, host, port, limit):
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_test(loop, code, host, port, limit))
    except Exception as ex:
        print("Exception %s" %ex)
        loop.call_soon_threadsafe(loop.stop)
        print(ex)
    except KeyboardInterrupt as ke:
        print("Exception %s" %ex)        
        loop.call_soon_threadsafe(loop.stop)
        print(ke)
    finally:
        loop.close()
    
if __name__=='__main__':
    run_eryo()
