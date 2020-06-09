import os, glob
from .watcher import Watcher
from .compile_tex import compile_tex


def compile_tex_watcher_callback(event_type, file_path):
  if '.tex' in file_path:
    compile_tex(file_path)


def main():
  print('Watching for changes to any .tex file the local directory')
  watcher_instance = Watcher(compile_tex_watcher_callback)
  watcher_instance.run()


if __name__ == '__main__':
  main()
