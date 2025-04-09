# Zabbix Pushgateway
Flask Edition

_Get the PHP edition at https://github.com/Neon6105/zabbix-pushgateway-php_
  
## Installation
1. Clone this repo to a server that sits between your push devices and Zabbix (can colo with Zabbix on a different port)  
1. Rename `example.config.py` to `config.py`  
1. Edit `config.py` to set the api_url and api_token for Zabbix

## Virtual Environment
TODO: Write documentation for virtual environments  

## Device Profiles
1. For each device type, create a _deviceprofile_.py in `profiles`  
   It is recommended to copy the provided template rather than creating the profile manually  
1. Modify the main section of the device profile to handle the incoming JSON file  
`host_key` is the key from the pushed JSON that contains the technical host name in Zabbix  
`key_prefix` is a string that will be prefixed to each JSON key before sending it to Zabbix  
`skip_key` is an iterable item of strings containing the JSON keys to ignore (will not be sent to Zabbix)  

## Zabbix Setup
1. Create a new host in Zabbix and set the host name to match the value provided by the host_tag key in the pushed JSON  
1. Create an Item for the host for each additional JSON key and set the type to "Zabbix Trapper".  
The item key must include the `KEY_PREFIX` from `config.py` and the `key_prefix` from the plugin, if set.  
```python
< config.py >

zabbix_vars = {...
"KEY_PREFIX": "pushed.",
...}
```
```python
< profiles/deviceprofile.py >

...
key_prefix = "device."
```
If the key from the pushed JSON is `metric1` then the Zabbix item key must be "pushed.device.metric1"  
To omit any portion of the prefix, simply set the value to an empty string  

## Device Setup
1. Configure your device to push its JSON file to your_server_url/deviceprofile

## Query Strings
The template allows setting the host name by query string. The item name must match the host_tag in the device profile  
Example using the template profile: http://zabbix.example.com:8080/template?host=myhost
