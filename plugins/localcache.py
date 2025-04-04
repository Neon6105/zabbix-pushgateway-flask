from _config import getvar
from flask import Blueprint, request
from os import makedirs
from os.path import isfile, join, basename
import json

# Display troubleshooting data for the localcache plugin
plugin_name = basename(__file__)[:-3]
blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["GET"])
def translate():
  plug = request.args.get("plugin")
  host = request.args.get("host")
  host = host if host else "localhost"

  file_cache = getvar("FILE_CACHE", "Unknown")
  debug_data = "<h2>localcache</h2>" \
    f"FILE_CACHE: {file_cache}<br />"
  if plug:
    parent_path, host_json = get_last(plug, host)
    debug_data = f"{debug_data}" \
      f"<h2>{plug} {' :: ' + host if host != 'localhost' else ''}</h2>" \
      f"Parent path: {parent_path}<br />" \
      f"File name: {host_json}<br />" \
      f"File exists: {True if isfile(join(parent_path, host_json)) else False}<br />"
  return debug_data
# -- end translate()


def readlocalcache(plug, host):
  parent_path, host_json = get_last(plug, host)
  if isfile(join(parent_path, host_json)):
    with open(join(parent_path, host_json), "r") as f:
      latest = json.load(f)
    return latest
  else:
    return_string = "No cache file for " + str(f"{host} (" if host else "") + \
                    plug + str(")" if host else "") + "!"
    return return_string
# -- end readlocalcache()


def writelocalcache(plug, host, query_string="", json_in={}, json_out={}, result={}):
  parent_path, host_json = get_last(plug, host)
  makedirs(parent_path, exist_ok=True)
  data = {
    "Query String": query_string,
    "Recevied JSON": json_in,
    "Zabbix JSON": json_out,
    "Zabbix Response": result,
  }
  with open(join(parent_path, host_json), "w") as f:
    json.dump(data, f, indent=4)
  return True
# -- end writelocalcache()


def get_last(plugin_name, host):
  return join(getvar("FILE_CACHE", "localcache"), plugin_name), f"{host}.json"
# -- end get_last
