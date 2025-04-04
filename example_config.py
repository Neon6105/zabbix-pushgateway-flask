from os import getenv
import os.name

_vars = {
  "ZPG_SKIP_PLUGINS":  ("template", ),

  "FILE_CACHE":        "C:\\Temp\\Pushgateway" if os.name == "nt" else "/tmp/pushgateway",

  "ZABBIX_ADDRESS":    "127.0.0.1",
  "ZABBIX_API_TOKEN":  "",
  "ZABBIX_KEY_PREFIX": "",
  "ZABBIX_USE_HTTPS":  False,
}


def getvar(varname, default=None):
  return getenv(varname, _vars.get(varname, default))
