import yaml
from os.path import expanduser, isfile
import os

getsecret_overrides = {}

def setsecret(key, value):
  getsecret_overrides[key] = value

def getsecret(key, default=None):
  if key in getsecret_overrides:
    return getsecret_overrides[key]
  environ_value = os.environ.get(key)
  if environ_value is not None:
    return environ_value
  secrets = {}
  if isfile('.getsecret.yaml'):
    secrets = yaml.load(open('.getsecret.yaml'), Loader=yaml.SafeLoader)
  elif isfile(expanduser('~/.getsecret.yaml')):
    secrets = yaml.load(open(expanduser('~/.getsecret.yaml')))
  else:
    if default is None:
      raise FileNotFoundError('cannot find .getsecret.yaml')
    return default
  if key not in secrets:
    if default is None:
      raise ValueError('.getsecret.yaml does not contain key ' + key)
    return default
  return secrets[key]
