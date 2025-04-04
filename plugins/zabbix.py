from _config import getvar
from flask import Blueprint
from os.path import basename
import json
import requests
import time

''' Zabbix
Design a ZabbixObject, used by plugins
'''
plugin_name = basename(__file__)[:-3]

address = getvar("ZABBIX_ADDRESS", default="localhost")
api_token = getvar("ZABBIX_API_TOKEN", default="")
key_prefix = getvar("ZABBIX_KEY_PREFIX", default="")
use_https = getvar("ZABBIX_USE_HTTPS", default=False)


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
    return datadict, result
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


# Display troubleshooting data for the Zabbix connection and object
blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["GET"])
def translate():
  zbx = ZabbixObject()
  debug_data = "" \
    "<h2>Plugin Variables</h2>" \
    f"Address: {address}<br />" \
    f"API token: {api_token}<br />" \
    f"Key prefix: {key_prefix}<br />" \
    f"Use HTTPS: {use_https}<br />" \
    "<br />" \
    "<h2>Object Variables</h2>" \
    f"API URL: {zbx.api_url}<br />" \
    f"Headers: {zbx.headers}<br />" \
    f"Key prefix: {zbx.key_prefix}<br />"
  return debug_data
# -- end translate()
