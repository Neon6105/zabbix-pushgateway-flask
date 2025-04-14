from flask import Blueprint, request
from os.path import basename
from outputs import Zabbix, readcache, writecache
from datetime import datetime
import calendar
import time

'''ENDEC
Receive and transform JSON pushed from Sage ENDEC units.
'''

plugin_name = basename(__file__)[:-3]
host_key = "facID"
plugin_prefix = f"{plugin_name}."  # set to "" for no prefix
skip_key = ("when", )
msg_data = ("srcInput", "srcName", "event", "orig", "stations")


def epochtime(isotime):
  if isotime:
    clock = datetime.fromisoformat(isotime)
    clock = calendar.timegm(clock.timetuple())
    clock = str(clock).split(".")[0]
  else:
    clock = str(time.time()).split(".")[0]
  return clock


# Flask Blueprint
blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["POST", "GET"])
def translate():
  host = request.args.get("host", None)
  host = host if host else request.args.get(host_key, None)
  if request.method == "POST":
    zbx = Zabbix()
    json_in = request.get_json()
    # Match the host_key to the technical host name in Zabbix
    host = host if host else json_in.get(host_key, None)
    if not host:
      return zbx.no_host(host_key, json_in)
    # Convert the incoming ISO 8601 string into epoch time (seconds)
    clock = json_in.get("when", None)
    clock = epochtime(clock)
    for _key, _val in json_in.items():
      if _key in skip_key:
        continue
      if _key == "msg":
        _key = f"msg{json_in['msgType']}"
      zbx.add_param(host, plugin_prefix, _key, str(_val), clock)
    # Special case: Alert Sent (msgType == 4)
    if (json_in["msgType"] == 4):
      event = json_in["event"]
      time_logged = epochtime(json_in["timeLogged"])
      for _key, _val in json_in["msg"].items():
        if (_key not in msg_data):
          continue
        if _key == "event":
          _key = _val
          _val = time_logged
        zbx.add_param(host, f"{event}{plugin_prefix}", _key, str(_val), time_logged)
    # -- end msgType == 4
    json_out, result = zbx.push()
    qs = request.query_string.decode("utf-8")
    writecache(plugin_name, host, qs, json_in, json_out, result.json())
    return result.content
  # implied else (it's a GET request)
  return readcache(plugin_name, host)
# -- end translate()
