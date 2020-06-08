from dataprotocols.gsof import Gsof
import asyncio
import functools
import os
import signal
import click
import json
import time

# TEST
CODE = 'HSCO'
IP = "hsco.dyndns.org"
PORT = 5018


async def run_test(loop, code, host, port, limit=2000):
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    gsof_test = "eryo_test.json"
    limit_counter = limit
    counter = 0    
    print("Conexion a->", ginput)
    gsof = Gsof(**ginput)
    print("GSOF object", gsof)
    idc = await gsof.connect()
    print("IDC->", idc)
    with open(gsof_test, "a+") as gsof_file:
        gsof_file.write("[")
        while counter <= limit_counter:
            try:
                print("Hard beat")
                print(gsof.hard_beat(idc))
                print("MSG recv>")
                await gsof.get_message_header(idc)
                print("Header msg->", gsof.msg_bytes)
                done, msg = await gsof.get_records()
                if done:
                    print("Eryo", msg)
                    json.dump(msg, gsof_file, indent=2)
                    gsof_file.write(",\n")
            except Exception as ex:
                gsof_file.write("]")
                print("Error %s" % ex)
                loop.close()
            except KeyboardInterrupt as ke:
                gsof_file.write("]")
                loop.close()
                print(ke)
            counter += 1
        gsof_file.write("]")



@click.command()
@click.option("--code", default="HSCO", help="Código de estación")
@click.option("--host", default="hsco.dyndns.org", help="URL de estación")
@click.option("--port", default=5018, help="Nro de puerto")
@click.option("--limit", default=2000, help="Nro de mensajes")
def run_gsof(code, host, port, limit):
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
    run_gsof()
