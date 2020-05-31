import time
import os

from .task import Task
from .utils import get_logger, set_logger

log = get_logger(__name__)


class TaskList:
  def __init__(self, wrkdir=None, autosync=False):
    self.wrkdir = wrkdir or '.'
    self.tasks = []
    self.autosync = autosync
    self.latest = None
    if self.autosync:
      self.make_wrkdir()
      self.load()
  
  def add(self, task):
    log.debug("Adding task %s", repr(task))
    self.tasks.append(task)
    self.sort_tasks()
    log.info("Added task %s, now %d tasks.", task, len(self))
    log.debug("Tasklist now: %s", self)
    if self.autosync:
      self.serialize()
    
  def sort_tasks(self):
    self.tasks = sorted(self.tasks, key=lambda x: x.ts)

  def __str__(self):
    return '%s@%s' % (self.wrkdir, str(self.tasks))

  def __len__(self):
    return len(self.tasks)

  def __bool__(self):
    return bool(self.tasks)

  def __iter__(self):
    return self.tasks.__iter__()

  def __next__(self):
    return self.tasks.__next__()

  def __eq__(self, b):
    return type(b) == type(self) and [t.ts for t in self] == [t.ts for t in b] and self.wrkdir == b.wrkdir

  def clear(self):
    log.debug("Clearing %d tasks from queue.", len(self.tasks)) # too verbose for info level, downgraded to debug level
    self.tasks = []
    if self.autosync:
      self.serialize()

  def run_all(self, skip_permanent_failures=False):
    while self.tasks:
      t = self.run_one()
      if t.succeeded():
        log.debug("Task %s succeded. %d more pending.", t, len(self.tasks)) # too verbose for info level, downgraded to debug level
      else:
        log.error("Task %s failed with %s error.", t.name, 'retriable' if t.failed_retry() else 'permanent')
        if skip_permanent_failures and not t.failed_retry():
          log.debug("Discarding perm-failed task and continuing with next (skip_permanent_failures=True)") # too verbose for info level, downgraded to debug level
          self.popleft()
          continue
        return False
    return True        
  
  def popleft(self, n=None):
    if n is None:
      n = 0
    t = self.tasks.pop(n)
    if self.autosync:
      self.serialize()
    return t
  
  def peek(self, n=None):
    if n is None:
      n = 0
    return self.tasks[n]

  def run_one(self):
    t = self.popleft(0)
    log.info("Running task %s", t)
    t.run()
    if not t.succeeded():
      self.add(t)
    elif self.autosync:
      self.serialize()
    self.latest = t
    return t

  def run_next(self):
    return self.run_one().succeeded()

  def succeeded(self):
    if self.latest is None:
      if not self.tasks:
        return True
      raise RuntimeError("No task executed yet.")
    return self.latest.succeeded()
  
  def failed_retry(self):
    if self.latest is None:
      if not self.tasks:
        return False
      raise RuntimeError("No task executed yet.")
    return self.latest.failed_retry()
  
  def age(self):
    if not self.tasks:
      return 0
    return time.time() - self.peek().ts

  def get_task_files(self):
    return sorted([os.path.join(self.wrkdir, fn) for fn in os.listdir(self.wrkdir) if fn.startswith('task@')], key=lambda x: float(x.split('@')[1]))

  def make_wrkdir(self):
    if os.path.exists(self.wrkdir):
      return
    try:
      os.makedirs(self.wrkdir)
    except OSError as e:
      log.error("Unable to create queue wrkdir %s: %s", self.wrkdir, e)

  def serialize(self):
    log.debug("Serializing %s tasks into '%s'", len(self), self.wrkdir) # too verbose for info level, downgraded to debug level
    self.make_wrkdir()
    # clear previous tasks
    exfiles = self.get_task_files()
    if exfiles:
      log.debug("Clearing %s previously existing task files.", len(exfiles)) # too verbose for info level, downgraded to debug level
      for f in exfiles:
        os.remove(f)
    # serialize current tasks
    for t in self.tasks:
      fname = os.path.join(self.wrkdir, "task@%s@%s" % (str(t.task_id), t.name))
      if os.path.exists(fname):
        log.debug("Skipping serialization of task '%s': %s already serialized", str(t), fname)
      else:
        log.debug("Serializing task '%s' -> %s", str(t), fname)
        with open(fname, 'w+') as f:
          f.write(t.serialize())
  
  def load(self):
    if not os.path.exists(self.wrkdir):
      log.error("Tasklist workdir '%s' does not exist. Skipping.", self.wrkdir)
      return
    for fname in self.get_task_files():
      task = Task.from_bytes(open(fname).read())
      self.tasks.append(task)
    self.sort_tasks()

