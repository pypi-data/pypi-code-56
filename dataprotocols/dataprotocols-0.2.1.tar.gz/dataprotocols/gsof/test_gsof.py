from dataprotocols.gsof import Gsof
import asyncio
import functools
import os
import signal
import click

# TEST
CODE = 'HSCO'
IP = "hsco.dyndns.org"
PORT = 5018


async def run_test(loop, code, host, port):
    ginput = dict(host=host,
                  port=port,
                  code=code,
                  timeout=5,
                  sock=None,
                  loop=loop)
    print("Conexion a->", ginput)
    gsof = Gsof(**ginput)
    print("GSOF object", gsof)
    idc = await gsof.connect()
    print("IDC->", idc)
    while True:
        try:
            print("Hard beat")
            print(gsof.hard_beat(idc))
            print("MSG recv>")
            await gsof.get_message_header(idc)
            print("Header msg->", gsof.msg_bytes)
            done, msg = await gsof.get_records()
            print(done, msg)
        except Exception as ex:
            print("Error %s" % ex)
            loop.close()
        except KeyboardInterrupt as ke:
            loop.close()
            print(ke)




@click.command()
@click.option("--code", default="HSCO", help="Código de estación")
@click.option("--host", default="hsco.dyndns.org", help="URL de estación")
@click.option("--port", default=5018, help="Nro de puerto")
def run_gsof(code, host, port):
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_test(loop, code, host, port))
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
