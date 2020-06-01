import subprocess
import os
from cement import Controller, ex
from github import Github
from rich.console import Console
from functools import partial
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)


class Updates(Controller):
    class Meta:
        label = 'updates'
        stacked_type = 'embedded'
        stacked_on = 'base'

    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
        )

    @ex(help='Checks local gh cli version')
    def local(self):
        res = subprocess.check_output(['gh', '--version'])
        version = res.split()[2].decode()
        Console().print('Local version: %s' % version, style='bold purple')
        return version

    @ex(help='Checks remote gh version')
    def remote(self):
        g = Github()
        version = g.get_repo('cli/cli').get_latest_release().title.split('v')[1]
        Console().print('Remote version: %s' % version, style='bold blue')
        return version

    def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
        """Copy data from a url to a local file."""
        response = urlopen(url)
        # This will break if the response doesn't contain content length
        self.progress.update(task_id, total=int(response.info()["Content-length"]))
        with open(path, "wb") as dest_file:
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                self.progress.update(task_id, advance=len(data))

    def get_file(self, url):
        with ThreadPoolExecutor(max_workers=4) as pool:
            filename = url.split("/")[-1]
            dest_path = os.path.join("./", filename)
            task_id = self.progress.add_task("download", filename=filename)
            pool.submit(self.copy_url, task_id, url, dest_path)

    @ex(help='Checks if new version is available')
    def check(self):
        res = self.local() == self.remote()
        if res:
            Console().print('You have the latest gh version installed', style='bold green')
        else:
            Console().print('A newer gh version is available', style='bold yellow')
            Console().print('Run \'ghupdate update\' to get the latest version', style='bold red')

    @ex(help='Downloads the latest gh version')
    def download(self):
        g = Github()
        assets = g.get_repo('cli/cli').get_latest_release().get_assets()
        for a in assets:
            if a.content_type == 'application/x-debian-package' and 'amd64' in a.name:
                fl = a.browser_download_url.split('/')[-1]
                self.get_file(a.browser_download_url)
                return (subprocess.run(['sudo', 'dpkg', '-i', fl]))

    @ex(help='Updates to the newer version')
    def update(self):
        res = self.local() == self.remote()
        if not res:
            self.download()
