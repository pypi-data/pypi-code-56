import logging
import subprocess

logger = logging.getLogger("megatools_wrapper")


class MegaToolsWrapper:
    megatools_path = ""

    def __init__(self, megatools_path=""):
        self.megatools_path = megatools_path

    def copy(
        self,
        remote_path="",
        local_path="",
        download=False,
        no_follow=False,
        enable_previews=False,
        disable_previews=False,
        disable_resume=False,
        username=None,
        password=None,
        reload=False,
        limit_speed=None,
        proxy=None,
        config=None,
        ignore_config_file=False,
    ):
        """
        Usage:
            megacopy.exe [OPTION] - synchronize local and remote mega.nz directories

        Help Options:
            -h, --help                  Show help options
            --help-all                  Show all help options

        Application Options:
            -r, --remote=PATH           Remote directory
            -l, --local=PATH            Local directory
            -d, --download              Download files from mega
            --no-progress               Disable progress bar
            --no-follow                 Don't follow symbolic links
            -n, --dryrun                Don't perform any actual changes
            --enable-previews           Generate previews when uploading file
            --disable-previews          Never generate previews when uploading file
            --disable-resume            Disable resume when downloading file
            -u, --username=USERNAME     Account username (email)
            -p, --password=PASSWORD     Account password
            --no-ask-password           Never ask interactively for a password
            --reload                    Reload filesystem cache
            --limit-speed=SPEED         Limit transfer speed (KiB/s)
            --proxy=PROXY               Proxy setup string
            --config=PATH               Load configuration from a file
            --ignore-config-file        Disable loading mega.ini
            --debug=OPTS                Enable debugging output
            --version                   Show version information
        """

        command = self.megatools_path
        command += "megadl"
        command += " "

        if remote_path:
            command += "--remote="
            command += remote_path
            command += " "

        if local_path:
            command += "--local="
            command += local_path
            command += " "

        if download:
            command += "--download"
            command += " "

        if no_follow:
            command += "--no-follow"
            command += " "

        if enable_previews:
            command += "--enable-previews"
            command += " "

        if disable_previews:
            command += "--disable-previews"
            command += " "

        if disable_resume:
            command += "--disable-resume"
            command += " "

        if username:
            command += "--username="
            command += username
            command += " "

        if password:
            command += "--password="
            command += password
            command += " "

        if reload:
            command += "--reload"
            command += " "

        if limit_speed:
            command += "----limit-speed="
            command += limit_speed
            command += " "

        if proxy:
            command += "--proxy="
            command += proxy
            command += " "

        if config:
            command += "--config="
            command += config
            command += " "

        if ignore_config_file:
            command += "--ignore_config_file"
            command += " "

        logger.debug(command)

        return_code = execute_command(command)

        logger.debug(return_code)

    def megadf(self, mega_link, limit_speed=0, path="./"):
        """
        Usage:
            megadf.exe [OPTION] - display mega.nz storage quotas/usage

        Help Options:
            -?, --help                  Show help options
            --help-all                  Show all help options

        Application Options:
            -h, --human                 Use human readable formatting
            --mb                        Show numbers in MiB
            --gb                        Show numbers in GiB
            --total                     Show only total available space
            --used                      Show only used space
            --free                      Show only available free space
            -u, --username=USERNAME     Account username (email)
            -p, --password=PASSWORD     Account password
            --no-ask-password           Never ask interactively for a password
            --reload                    Reload filesystem cache
            --limit-speed=SPEED         Limit transfer speed (KiB/s)
            --proxy=PROXY               Proxy setup string
            --config=PATH               Load configuration from a file
            --ignore-config-file        Disable loading mega.ini
            --debug=OPTS                Enable debugging output
            --version                   Show version information
        """

        # TODO

        command = f"{self.megatools_path}megacopy {mega_link} --limit-speed={limit_speed} --path={path}"

        logger.debug(command)

        return_code = execute_command(command)

        logger.debug(return_code)

    def megadl(
        self,
        mega_link,
        path=None,
        disable_resume=False,
        username=None,
        password=None,
        reload=False,
        limit_speed=0,
        proxy=None,
        config=None,
        ignore_config_file=False,
    ):
        """
        Usage:
            megadl.exe [OPTION] - download exported files from mega.nz

        Help Options:
            -h, --help                  Show help options
            --help-all                  Show all help options

        Application Options:
            --path=PATH                 Local directory or file name, to save data to
            --no-progress               Disable progress bar
            --print-names               Print names of downloaded files
            --choose-files              Choose which files to download when downloading folders (interactive)
            --disable-resume            Disable resume when downloading file
            -u, --username=USERNAME     Account username (email)
            -p, --password=PASSWORD     Account password
            --no-ask-password           Never ask interactively for a password
            --reload                    Reload filesystem cache
            --limit-speed=SPEED         Limit transfer speed (KiB/s)
            --proxy=PROXY               Proxy setup string
            --config=PATH               Load configuration from a file
            --ignore-config-file        Disable loading mega.ini
            --debug=OPTS                Enable debugging output
            --version                   Show version information
        """

        command = self.megatools_path
        command += "megadl"
        command += " "
        command += mega_link
        command += " "

        if path:
            command += "--path="
            command += path
            command += " "

        if disable_resume:
            command += "--disable-resume"
            command += " "

        if username:
            command += "--username="
            command += username
            command += " "

        if password:
            command += "--password="
            command += password
            command += " "

        if reload:
            command += "--reload"
            command += " "

        if limit_speed:
            command += "----limit-speed="
            command += limit_speed
            command += " "

        if proxy:
            command += "--proxy="
            command += proxy
            command += " "

        if config:
            command += "--config="
            command += config
            command += " "

        if ignore_config_file:
            command += "--ignore_config_file"
            command += " "

        logger.debug(command)

        return_code = execute_command(command)

        logger.debug(return_code)


def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    return process.returncode


if __name__ == "__main__":
    formatter = logging.Formatter(
        "%(asctime)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(stream_handler)

    wrapper = MegaToolsWrapper(megatools_path="D:\\megatools\\")

    wrapper.megadl(
        "https://mega.nz/#!p05w1QYS!o1_0olFXawso2qm1t9pDCNN8jOaOvod-zosaa_C2Ym0", "./"
    )
