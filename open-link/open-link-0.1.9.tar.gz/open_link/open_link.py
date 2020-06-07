
import subprocess


def open_in_chrome(url):
    subprocess.call(['google-chrome', '--new-window', url])
    return True
