from config import cache_vars
from flask import Blueprint, request
from os import makedirs, getcwd
from os.path import isfile, join, basename
import json


plugin_name = basename(__file__)[:-3]
cache_dir = cache_vars.get("CACHE_DIR", join(getcwd(), "cache"))

blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["GET"])
def read_local_cache():
  plug = request.args.get("profile")
  host = request.args.get("host")
  host = host if host else "localhost"
  debug_data = "<h2>localcache</h2>" \
    f"Cache Directory: {cache_dir}<br />"
  if plug:
    parent_path, host_json = get_last(plug, host)
    debug_data = f"{debug_data}" \
      f"<h2>{plug} {' :: ' + host if host != 'localhost' else ''}</h2>" \
      f"Profile cache: {parent_path}<br />" \
      f"File name: {host_json}<br />" \
      f"File exists: {True if isfile(join(parent_path, host_json)) else False}<br />"
  else:
    debug_data = f"{debug_data}" \
      f"<h2>{host}</h2>" \
      f"Please specify a connection profile for {host}. " \
      f"e.g. ?host={host}&profile=default<br />"
  return debug_data
# -- end translate()


def readcache(plug, host):
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


def writecache(plug, host, query_string="", json_in={}, json_out={}, json_result={}):
  parent_path, host_json = get_last(plug, host)
  makedirs(parent_path, exist_ok=True)
  data = {
    "Query String": query_string,
    "Received JSON": json_in,
    "Pushed JSON": json_out,
    "Zabbix Response": json_result,
  }
  with open(join(parent_path, host_json), "w") as f:
    json.dump(data, f, indent=4)
  return True
# -- end writelocalcache()


def get_last(plugin_name, host):
  return join(cache_dir, plugin_name), f"{host}.json"
# -- end get_last
