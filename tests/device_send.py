#!/usr/bin/env python3
import requests
import sys
import time


data = {
  "timestamp": time.time(),
  "snum": "X123456",
  "host": "iamdevice",
  "facID": "iamdevice",
  "ip": "192.168.144.120",
  "bool0": False,
  "bool1": True,
  "integer": 1234,
  "string": "this is some data",
}


if __name__ == "__main__":
  if len(sys.argv) > 1:
    endpoint = sys.argv[-1]
  else:
    endpoint = "default"
  url = f"http://localhost:5000/{endpoint}"
  headers = {'Content-Type': 'application/json'}
  response = requests.post(url, headers=headers, json=data)
  print(response)
  # print(response.content)
  # print(response.text)
  # print(response.reason)
  # print(response.request)
  # print(response.url)
