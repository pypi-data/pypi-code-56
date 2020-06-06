from jsondiff import diff
import time

""" Compare two json objects and return true if they are deeply equal """
def isjsonequal(base, obj):
  result = diff(base, obj)
  keys = len(result.keys())
  return keys == 0

"""
Function to wait until the kafka client is accesible.
Do not return until it can get the client info.
"""
def wait_for_client_info(client, timeout=600):
  start = time.time()
  while time.time() - start < timeout:
      time.sleep(1)
      try:
        response = client.get_cluster_info()
        if response['kafka_cluster_id']:
          return response['kafka_cluster_id']
      except:
          print('[+] Waiting for Kafka Connect to be ready...')

  raise RuntimeError('[-] Kafka Connect client timeout exceeded')
