from flask import Flask, request, abort
import time

app = Flask(__name__)


@app.route('/zabbix/api_jsonrpc.php', methods=['POST'])
def index():
  posted = request.get_json()
  if not posted:
    abort(500, "No JSON received")
  params = posted.get("params", {})
  zabbix_reply = {"jsonrpc": "2.0"}
  if not params:
    zabbix_reply["result"] = "No parameters received."
  else:
    result = []
    for param in params:
      result.append({"host": param["host"], "item": "28356"})
    zabbix_reply["result"] = result
  zabbix_reply["id"] = int(str(time.time()).split(".")[0])
  return zabbix_reply


if __name__ == '__main__':
  app.run(port=80)
