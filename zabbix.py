import json
import os
import requests
import time

''' Zabbix
Design a ZabbixObject, used by plugins
'''
conf_json = 'zabbix.conf.json'

''' Editing below this line should not be necessary for normal operation. '''

# Load configs. Priority order is environmental variable, config file, then hard-coded defaults
try:
  with open(conf_json, 'r') as f:
    conf = json.load(f)
except FileNotFoundError:
  conf = dict()
finally:
  # os.getenv("ZABBIX_VARIABLE", conf.get("variable", "default-value"))
  # ^ environmental variable     ^ config file        ^ hard-coded default
  address = os.getenv("ZABBIX_ADDRESS", conf.get("address", "127.0.0.1"))
  api_token = os.getenv("ZABBIX_API_TOKEN", conf.get("api_token", ""))
  key_prefix = os.getenv("ZABBIX_KEY_PREFIX", conf.get("key_prefix", ""))
  use_https = os.getenv("ZABBIX_USE_HTTPS", conf.get("use_https", False))
# -- end Load configs


class ZabbixObject:
  def __init__(self):
    self.params = list()
    self.api_url = "http" + str("s" if use_https else "") + f"://{address}/zabbix/api_jsonrpc.php"
    self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    self.key_prefix = key_prefix

  def add_param(self, host, plugin_prefix, key, value, clock=None, ns=0):
    if not clock:
      clock, ns = str(time.time()).split(".")
    if not plugin_prefix:
      plugin_prefix = ""
    if host and key and value and clock:
      self.params.append({
        "host": host,
        "key": self.key_prefix + plugin_prefix + key,
        "value": value,
        "clock": int(clock),
        "ns": int(ns)
      })
      return True
    else:
      return False
  # -- end add_param()

  def push(self):
    datadict = {
      "jsonrpc": "2.0",
      "method": "history.push",
      "params": self.params,
      "id": int(str(time.time()).split('.')[0])
    }
    data = json.dumps(datadict)
    result = requests.post(self.api_url, headers=self.headers, data=data)
    print(result.content)
  # -- end push()

  def failure(self, reason, details):
    return {
      "Status": 1,
      "Result": "Failure",
      "Reason": reason,
      "Details": details,
    }
  # -- end failure()

  def no_host(self, tag, details=""):
    return self.failure(f"Unable to identify host using \'{tag}\'", details=details)
  # -- end no_host()
# -- end ZabbixObject
