from flask import Blueprint
import json
import os
import requests
import time

''' Zabbix
Variables, connection data, and a ZabbixObject, used by plugins
'''

# Address and (optional) port of the Zabbix web interface
address = "127.0.0.1"

# Attempt to load the Zabbix API key from the environment
# TODO: Add more supported locations to search for the API token (dotenv, file)
# TODO: Error correction if no API token is found
api_token = os.getenv("ZABBIX_TOKEN", default="")

# Set to True if your web interface has a working SSL certificate
use_https = False

''' Editing below this line should not be necessary for normal operation. '''

# Register a Blueprint to display Zabbix connection info
# Currently unused. Preemptive in case zabbix.py gets moved to 'plugins'
blueprint = Blueprint("zabbix", __name__)


@blueprint.route("/zabbix", methods=["GET"])
def translate():
  print(f"Address: {address}")
  print(f"api_token: {api_token}")
  print(f"use_https: {use_https}")
# -- end translate()


class ZabbixObject:
  def __init__(self):
    self.params = list()
    self.api_url = "http" + str("s" if use_https else "") + f"://{address}/zabbix/api_jsonrpc.php"
    self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}

  def add_param(self, host, key, value, clock=None, ns=0):
    if not clock:
      clock, ns = str(time.time()).split('.')
    if host and key and value and clock:
      self.params.append({
        "host": host,
        "key": key,
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
