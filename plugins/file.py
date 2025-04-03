from os import makedirs
from os.path import isfile, join
import json

localcache = "localcache"  # Recommend using /tmp/localcache

# TODO: Update plugins to use outfile (plugins.outfile.w ?? or import plugins.outfile as outfile)


def readlocal(plugin_name, host):
  parent_path, host_json = get_last(plugin_name, host)
  if isfile(join(parent_path, host_json)):
    with open(join(parent_path, host_json), "r") as f:
      latest = json.load(f)
    return latest
  else:
    return_string = "No cache file for " + str(f"{host} (" if host else "") + \
                    plugin_name + str(")" if host else "") + "!"
    return return_string


def writelocal(plugin_name, host, query_string="", json_in={}, json_out={}, reply={}):
  parent_path, host_json = get_last(plugin_name, host)
  makedirs(parent_path, exist_ok=True)
  data = {
    "Query String": query_string,
    "Recevied JSON": json_in,
    "Zabbix JSON": json_out,
    "Zabbix Response": reply,
  }
  with open(join(parent_path, host_json), "w") as f:
    json.dump(data, f, indent=4)
  return True


def get_last(plugin_name, host):
  return join(localcache, plugin_name), f"{host}.json"
