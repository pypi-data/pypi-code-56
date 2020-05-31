import base64
import logging
import warnings
import click
from .run import run_xlsx_config
from .template import browserctrl_xlsx_template_data

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)


@click.group()
def main():
    """Browser automation toolset.
    """
    pass

@main.command(name="run-xlsx-config")
@click.option("-l", "--log", default="browserctrl.log", help="Log filename, default to browserctrl.log.")
@click.option("-s", "--sheet", help="Sheet name of config xlsx file. Default to the active sheet.")
@click.option("-v", "--variables-sheet", help="Sheet name of variables xlsx file. Default to the active sheet.")
@click.option("-r", "--repeat", default=1, type=int, help="Repeat times to run. Default to 1 means run only once.")
@click.option("-d", "--delay", default=5, type=int, help="Seconds delay before the next browser instance starts. Default to 5 seconds.")
@click.argument("config_xlsx_path", nargs=1, required=True)
@click.argument("variables_xlsx_path", nargs=1, required=False)
def run_xlsx_config_app(log, repeat, delay, config_xlsx_path, sheet, variables_xlsx_path, variables_sheet):
    """Run browser automation commands defined in xlsx file.
    """
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log),
        ])
    for counter in range(repeat):
        logging.info("run_xlsx_config counter: {}/{}".format(counter + 1, repeat))
        try:
            run_xlsx_config(config_xlsx_path, sheet, variables_xlsx_path, variables_sheet, delay)
        except Exception as error:
            logger.exception("run_xlsx_config got failed: {0}".format(error))

@main.command(name="create-xlsx-template")
@click.argument("output", nargs=1, required=False)
def create_xlsx_template_app(output):
    """Create a new xlsx file with command define template.
    """
    if not output:
        output = "browserctrl-xlsx-template.xlsx"
    with open(output, "wb") as fobj:
        fobj.write(base64.decodebytes(browserctrl_xlsx_template_data))

if __name__ == "__main__":
    main()