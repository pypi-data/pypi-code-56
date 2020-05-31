import json
import subprocess
import time
import tempfile

from .utils import get_logger, set_logger

log = get_logger(__name__)

class Task:
  def __init__(self, cmd, args=[], stdin=None, cwd=None, env={}, name=None):
    self.ts = time.time()
    self.task_id = '%.6f' % self.ts
    self.name = name or cmd
    if args is None:
      args = []
    self.cmd = {
      'command': cmd,
      'args': args,
      'stdin': stdin,
      'cwd': cwd,
      'env': env,
    }
    self.status = {
      'startts': None,
      'runtime_s': None,
      'returncode': None,
      'stdout': None,
      'stderr': None,
    }
    log.debug("Built task '%s'", self)
  
  def __eq__(self, b):
    for prop in ['ts', 'name', 'cmd']:
      if getattr(self, prop) != getattr(b, prop):
        return False
    return True

  def __str__(self):
    return "%s@%s" % (self.task_id, self.name)

  def __repr__(self):
    return '|'.join(str(x) for x in [self.task_id, self.name, self.cmd, self.status])

  def get_cmd(self):
    return [self.cmd['command']] + self.cmd['args']

  def get_stdin(self):
    return self.cmd['stdin']
  
  def get_env(self):
    return self.cmd['env']
  
  def get_cwd(self):
    return self.cmd['cwd']

  def run(self):
    """Execute the task."""
    if type(self.cmd['command']) is not str:
      raise ValueError('Invalid command provided! Need string, got %s', type(self.cmd['command']))
    cmdline = [self.cmd['command']]
    cmdline.extend(self.cmd['args'])
    # create files for stdout and stderr
    with tempfile.TemporaryFile() as sout:
      with tempfile.TemporaryFile() as serr:
        p = subprocess.Popen(cmdline, cwd=self.cmd['cwd'], env=self.cmd['env'], stdin=self.cmd['stdin'], stdout=sout, stderr=serr)
        self.status['startts'] = time.time()
        log.debug("Starting task '%s': %s", self, cmdline) # too verbose for info level, downgraded to debug level
        p.communicate()
        # done!
        self.status['runtime_s'] = time.time() - self.status['startts']
        self.status['returncode'] = p.returncode
        log.debug("Exited %s in %ss", self.status['returncode'], round(self.status['runtime_s'], 2)) # too verbose for info level, downgraded to debug level
        sout.seek(0)
        serr.seek(0)
        self.status['stdout'] = sout.read().strip()
        self.status['stderr'] = serr.read().strip()
        if not self.succeeded() and self.status['stderr']:
          log.error("Task %s failed: stderr was '%s'", self, self.status['stderr'])
        elif self.status['stdout']:
          log.info("Task %s succeeded with message: '%s'", self, self.status['stdout'])

    return self.succeeded()

  def succeeded(self):
    """Return whether the process execution terminated successfully.
    Raises RuntimeError if process wasn't started."""
    if self.status['returncode'] is None:
      raise RuntimeError("Task '%s'@%s not executed yet.", self)
    return self.status['returncode'] == 0
  
  def failed_retry(self):
    """Return True if failed and returncode > 1"""
    if self.succeeded():
      return False
    return self.status['returncode'] > 1

  def serialize(self):
    return json.dumps({
      'ts': self.ts,
      'name': self.name,
      'task_id': str(self.task_id),
      'cmd': self.cmd,
    })
  
  @classmethod
  def from_bytes(cls, b):
    j = json.loads(b)
    rawt = cls('x')
    rawt.ts = j['ts']
    rawt.name = j['name']
    rawt.task_id = j['task_id']
    rawt.cmd = j['cmd']
    return rawt