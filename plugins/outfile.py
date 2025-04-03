from os.path import isfile, join

cache_dir = "local_cache"

# TODO: Save plugin.latest and host.latest in cache_dir/plugin_name
# TODO: Save input, output, and Zabbix reply for debugging
# TODO: Optional: Save as txt, csv, json, yaml, pickle, etc
# TODO: Use outfile to create Flask Templates
# TODO: Update plugins to use outfile (plugins.outfile.w ?? or import plugins.outfile as outfile)

'''
cache_data = {
  "input": {input from plugin},
  "output": {JSON to Zabbix},
  "zabbix": {reply from Zabbix API}
}
file.write(json_encode(cache_data))
'''


def w(plugin_name, data, host=None):
  file_path = get_latest(plugin_name, host)
  with open(file_path, "w") as file:
    file.write(data)
  return True


def r(plugin_name, host=None):
  file_path = get_latest(plugin_name, host)
  if isfile(file_path):
    with open(file_path, "r") as file:
      return file.read()
  else:
    return_string = "No cache file for " + str(f"{host} (" if host else "") + \
                    plugin_name + str(")" if host else "") + "!"
    return return_string


def get_latest(plugin_name, host=None):
  plugin_latest = join(cache_dir, f"{plugin_name}")
  host_latest = join(cache_dir, plugin_name, f"{host}")
  return host_latest if host else plugin_latest
