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

def epochtime(isotime):
  if clock:
    clock = datetime.fromisoformat(clock)
    clock = calendar.timegm(clock.timetuple())
    clock = str(clock).split(".")[0]
  else:
    clock = str(time.time()).split(".")[0]

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
    for _key, _val in json_in.items():
      # TODO: handle 'msg' key
      if _key in skip_key:
        continue
      zbx.add_param(host, plugin_prefix, _key, str(_val), clock)
    json_out, result = zbx.push()
    qs = request.query_string.decode("utf-8")
    writecache(plugin_name, host, qs, json_in, json_out, result.json())
    return result.content
  # implied else (it's a GET request)
  return readcache(plugin_name, host)
# -- end translate()
