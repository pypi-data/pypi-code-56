"""
Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

from statis.hardware import memory
from statis.notification import Notification
from statis.notifier_types.memory import MemoryNotifier


class Used(MemoryNotifier):
    """A notifier for the currently used memory."""

    def get_description(self) -> str:
        return 'Display the current memory usage.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.get_used(),
                                            memory.get_total())
        return Notification('Used Memory', content)


class Free(MemoryNotifier):
    """A notifier for the currently available memory."""

    def get_description(self) -> str:
        return 'Display the currently available memory.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.get_available(),
                                            memory.get_total())
        return Notification('Available Memory', content)


class UsedSwap(MemoryNotifier):
    """A notifier for the currently used swap space."""

    def get_description(self) -> str:
        return 'Display the current swap space usage.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.get_used_swap(),
                                            memory.get_total_swap())
        return Notification('Used Swap', content)


class FreeSwap(MemoryNotifier):
    """A notifier for the currently free swap space."""

    def get_description(self) -> str:
        return 'Display the currently free swap space.'

    def run(self) -> Notification:
        content: str = self._format_content(memory.get_free_swap(),
                                            memory.get_total_swap())
        return Notification('Free Swap', content)
