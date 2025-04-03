from flask import Blueprint, request
from os.path import basename
from zabbix import ZabbixObject

plugin_name = basename(__file__)[:-3]
host_tag = 'hostname'
key_prefix = f'{plugin_name}.'

'''JSON
Pseudo-universal JSON reader. Tries to guess the host if not specified.
'''

blueprint = Blueprint(f'{plugin_name}', __name__)


@blueprint.route(f'/{plugin_name}', methods=['POST'])
def translate():
  zbx = ZabbixObject()
  posted = request.get_json()
  host = posted.get(host_tag, request.args.get(host_tag))
  if not host:
    return zbx.no_host(host_tag, posted)
  zbx.push()
  return f'{plugin_name} Blueprint'
