#!/bin/python3
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


class Watcher:
  def __init__(self, event_callback):
    self.set_logger_format()
    self.observer = Observer()
    self.watch_directory = self.determine_watch_directory()
    self.event_handler = FileChangeHandler(event_callback)

  def run(self):
    self.observer.schedule(self.event_handler, self.watch_directory, recursive=True)
    self.observer.start()
    self.keep_alive()

  def determine_watch_directory(self):
    return sys.argv[1] if len(sys.argv) > 1 else '.'

  def set_logger_format(self):
    logging.basicConfig(
      level = logging.INFO,
      format = '%(asctime)s - %(message)s',
      datefmt = '%Y-%m-%d %H:%M:%S',
    )

  def keep_alive(self):
    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      self.observer.stop()
    self.observer.join() 


class FileChangeHandler(FileSystemEventHandler):
  def __init__(self, event_callback):
    self.event_callback = event_callback

  def on_any_event(self, event):
    if event.is_directory:
      return None
    self.event_callback(event.event_type, event.src_path)


def sample_callback(event_type, file_path):
  if event_type == 'created':
    print("Watchdog received created event - {}".format(file_path))

  elif event_type == 'modified': 
    print("Watchdog received modified event - {}".format(file_path))
