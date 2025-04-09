from config import zabbix_vars
from flask import Blueprint
import json
import requests
import time

''' Zabbix
Design a ZabbixObject, used by plugins
'''
plugin_name = "zabbix"

api_url = zabbix_vars.get("API_URL", "http://localhost/zabbix/api_jsonrpc.php")
api_token = zabbix_vars.get("API_TOKEN", "")
key_prefix = zabbix_vars.get("KEY_PREFIX", "")


class Zabbix:
  def __init__(self):
    self.params = list()
    self.api_url = api_url
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
    json_out = {
      "jsonrpc": "2.0",
      "method": "history.push",
      "params": self.params,
      "id": int(str(time.time()).split('.')[0])
    }
    data = json.dumps(json_out)
    result = requests.post(self.api_url, headers=self.headers, data=data)
    return json_out, result
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
  zbx = Zabbix()
  debug_data = "" \
    "<h2>Plugin Variables</h2>" \
    f"API URL: {api_url}<br />" \
    f"API token: {api_token}<br />" \
    f"Key prefix: {key_prefix}<br />" \
    "<br />" \
    "<h2>Object Variables</h2>" \
    f"API URL: {zbx.api_url}<br />" \
    f"Headers: {zbx.headers}<br />" \
    f"Key prefix: {zbx.key_prefix}<br />"
  return debug_data
# -- end translate()
