'''
Console script for inout_scan.
'''

# import sys
import click
from inout_scan import inout_scan

DEFAULT_SERIAL_PORT = '/dev/ttyACM0'
DEFAULT_BAUDRATE = 9600


@click.group()
@click.version_option()
def main():
    """Gather bar codes from a scanner connected to the serial port and pass
       them to the InOut API. A local cache is maintained to be able to handle
       communication problems. Use the flush command to communicate unsubmitted
       bar codes."""


@main.command()
@click.option('--serial_port',
              default=DEFAULT_SERIAL_PORT,
              show_default=True,
              help='Serial port device that the barcode scanner is'
                   ' connected to.')
@click.option('--baud_rate',
              default=DEFAULT_BAUDRATE,
              show_default=True,
              help='Serial baud rate of the bar code scanner.')
@click.option('--api_url',
              required=True,
              help='InOut API url.')
@click.option('--api_key',
              help='InOut API key.')
@click.option('--scanner',
              required=True,
              help='Unique scanner name, ie: "reception1".')
def scan(serial_port, baud_rate, api_url, api_key, scanner):
    """Listen for strings from a barcode scanner connected to the (virtual)
       serial port and make an API call to InOut for each scanned code."""
    app = inout_scan.InOutScan()
    app.set_api(api_details={
        'api_url': api_url,
        'api_key': api_key,
    })
    app.set_scanner(scanner)
    app.set_serial(serial_details={
        'port': serial_port,
        'baudrate': baud_rate,
    })
    app.scan()


@main.command()
@click.option('--api_url',
              required=True,
              help='InOut API url.')
@click.option('--api_key',
              help='InOut API key.')
def flush(api_url, api_key):
    """
    Flush unsubmitted data to the api
    """
    app = inout_scan.InOutScan()
    app.set_api(api_details={
        'api_url': api_url,
        'api_key': api_key,
    })
    app.flush()


if __name__ == '__main__':
    main(auto_envvar_prefix='INOUT')
