import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import platform
import os, sys
from jinja2 import Environment, FileSystemLoader
import subprocess

host = platform.uname()[1]

consul_host = 'consul1'
consul_port = 8500
consul_node_url = 'http://' + consul_host + ':' + str(consul_port) + '/v1/catalog/node/'

"""
Example return payload from Consul:
{"Node":{"ID":"","Node":"web-node-01","Address":"172.16.100.101","Datacenter":"qlab01","TaggedAddresses":null,"Meta":{"somekey":"somevalue"},"CreateIndex":71,"ModifyIndex":71},"Services":{"web":{"ID":"web","Service":"web","Tags":["web"],"Address":"172.16.100.101","Port":80,"EnableTagOverride":false,"CreateIndex":71,"ModifyIndex":361}}}
"""

def getRole(host):
  try:
    # print 'About to go to URL:', consul_node_url + host
    consul_raw_data = requests.get(consul_node_url + host, verify=False)
    node_data = json.loads(consul_raw_data.text)
    # print node_data
  except:
    return None
  if node_data is not None:
    roles = []
    for service in node_data['Services'].iteritems():
      for (service_name, service_data) in [service]:
        for tag in service_data['Tags']:
          roles.append(tag)
    return roles
  else:
    return None

def writeConfig(roles):
  env = Environment(loader=FileSystemLoader('/',encoding='ascii'))
  template = env.get_template('/tmp/client.json.j2')
  output = template.render(roles=json.dumps(roles))
  with open("/etc/sensu/conf.d/client.json", "wb") as config_file:
    config_file.write(output)
  subprocess.call('pgrep sensu-client | xargs kill', shell=True)

def createSubscriptions():
  roles = getRole(host)
  update_subscriptions = False
  if roles is not None:
    try:
      client_config = open('/etc/sensu/conf.d/client.json', 'r').read()
    except IOError:
      print 'No existing config file. Creating it now...'
      writeConfig(roles)
      return
    client_config_json = json.loads(client_config)
    subscriptions = client_config_json['client']['subscriptions']
    for role in roles:
      if role not in subscriptions:
        subscriptions.append(role)
        update_subscriptions = True
    if update_subscriptions:
      print 'New roles found:', roles
      writeConfig(roles)
    else:
      print 'No new roles found'
  else:
    print 'Either no services exist in Consul for this host or the host is not in Consul at all.\nPlease seed the host in Consul via the seed-consul.sh script.'
    sys.exit(1)

if __name__ == "__main__":
    # execute only if run as a script
    createSubscriptions()

