import sys
import requests
import json
import argparse

# Example raw data: https://gist.githubusercontent.com/joemiller/1723079/raw/bb862b599fa7254a770bd00fc7b16ab24f164c3f/sensu-handler-input-example.json
event = json.load(sys.stdin)
host = event['client']['name']
client_ip = event['client']['address']

parser = argparse.ArgumentParser(description='Registers and updates services in Consul based on Sensu state transitions')
parser.add_argument('--consul', dest='consul', help='Base URI for Consul, including protocol and port (e.g.: http://my-consul.example.com:8500')
parser.add_argument('--datacenter', dest='datacenter', help='Name of the Consul datacenter where this service should be created/updated')

args = parser.parse_args()
datacenter = args.datacenter
consul_host = args.consul

def updateConsulService(event):
  consul_service_name =  event['check']['service_registry']['service_name']
  consul_service_port =  event['check']['service_registry']['port']
  consul_service_tags =  event['check']['service_registry']['tags']
  consul_output = event['check']['output']
  status = event['check']['status']
  if status == 0:
    consul_service_status = 'passing'
  else:
    consul_service_status = 'failing'
  data = { "Datacenter": datacenter, "Node": host, "Address": client_ip, "Service": { "Service": consul_service_name, "Tags": consul_service_tags, "Address": client_ip, "Port": consul_service_port }, "Check": { "Node": host, "CheckID": consul_service_name + ":" + host, "Name": "sensu-driven check", "Status": consul_service_status, "ServiceID": consul_service_name, "Output": consul_output }  }
  data_payload = json.dumps(data)
  headers = { 'Content-Type': 'application/json'}
  update_service = requests.put(consul_host + '/v1/catalog/register', headers=headers, data=data_payload)


if __name__ == "__main__":
  # execute only if run as a script
  updateConsulService(event)
