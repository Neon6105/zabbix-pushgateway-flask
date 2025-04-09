import os

zabbix_vars = {
  "API_URL": "http://localhost/zabbix/api_jsonrpc.php",
  "API_TOKEN": "",
  "KEY_PREFIX": "",
}
cache_vars = {
  "CACHE_DIR": "C:\\Temp\\zabbixpushgateway" if os.name == "nt" else "/tmp/zabbixpushgateway",
}
