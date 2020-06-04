"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import pathlib
import re
from typing import List, Optional, Tuple

from statis.notification import Notification
from statis.notifier import Notifier, NotifierError

PS_SYSFS_PATH: pathlib.Path = pathlib.Path('/sys/class/power_supply/')


def _get_current_charge(battery: pathlib.Path) -> int:
    """
    Return the given battery's current charge in percent.

    :param battery: The device path of the battery to query
    :return: The battery's current charge in percent
    """
    capacity_file = next(file for file in battery.iterdir()
                         if file.name == 'capacity')
    return int(capacity_file.read_text())


def _find_battery(bat_num: Optional[int]) -> Tuple[pathlib.Path, int]:
    """
    Find either the first battery or one with the given device number.

    :param bat_num: A battery to retrieve or None to return the first
    :return: A tuple with the found battery's sysfs path and number
    :raises NotifierError: if no battery could be found
    """
    batteries: List[Tuple[pathlib.Path, int]] = [
        (path, int(re.search(r'\d+$', path.name).group()))
        for path in sorted(PS_SYSFS_PATH.iterdir())
        if (path / 'capacity').exists()
    ]

    if not batteries:
        raise NotifierError('No batteries could be found the system.')

    if bat_num is None:
        battery = batteries[0]
    else:
        try:
            battery = next(b for b in batteries if b[1] == bat_num)
        except StopIteration:
            raise NotifierError(f'Battery {bat_num} does not exist.')

    return battery


class Charge(Notifier):
    """A notifier for the current charge of a given battery."""

    def __init__(self) -> None:
        super().__init__()

        self.bat_num: Optional[int] = None
        self.show_number: bool = False

    def get_description(self) -> str:
        return 'Display the current battery charge.'

    def add_args(self) -> None:
        self.parser.add_argument('-b', '--battery', type=int, metavar='N',
                                 help='a battery whose charge to display\n'
                                      '(default: the first battery found)')
        self.parser.add_argument('-n', '--show-number', action='store_true',
                                 help='include the battery no. in the title')

    def handle_args(self, args: argparse.Namespace) -> None:
        if args.battery is not None and args.battery < 0:
            self.parser.error('The battery number must be positive.')

        self.bat_num = args.battery
        self.show_number = args.show_number

    def run(self) -> Notification:
        found_path, found_num = _find_battery(self.bat_num)

        title: str = 'Battery Charge'
        if self.show_number:
            title += f' ({found_num})'

        return Notification(title, f'{_get_current_charge(found_path)} %')
