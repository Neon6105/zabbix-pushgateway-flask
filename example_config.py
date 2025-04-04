from os import getenv
import os.name

_vars = {
  "ZPG_SKIP_PLUGINS":  ("template", "localcache"),

  "FILE_CACHE":        "C:\\Temp\\Pushgateway" if os.name == "nt" else "/tmp/pushgateway",

  "ZABBIX_ADDRESS":    "127.0.0.1",
  "ZABBIX_API_TOKEN":  "3a5ae07dcdc53afd8b4e2a521161a03f7353ac6f09c19def87505e21a69501a6",
  "ZABBIX_KEY_PREFIX": "",
  "ZABBIX_USE_HTTPS":  False,
}


def getvar(varname, default=None):
  return getenv(varname, _vars.get(varname, default))
