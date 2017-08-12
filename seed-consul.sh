#!/bin/bash

# Script to pre-register LAMP stack endpoints

curl -XPUT  -H 'Content-Type: application/json' -d '{"Node": "web-node-01", "Datacenter": "qlab01", "NodeMeta": {"somekey": "somevalue"}, "Service": {"Address": "172.16.100.101", "Port": 80, "Service": "web", "Tags": [ "web", "bitcoin" ]}, "Address": "172.16.100.101" }' 'http://localhost:8500/v1/catalog/register'

curl -XPUT  -H 'Content-Type: application/json' -d '{"Node": "web-node-02", "Datacenter": "qlab01", "NodeMeta": {"somekey": "somevalue"}, "Service": {"Address": "172.16.100.102", "Port": 80, "Service": "web", "Tags": [ "web" ]}, "Address": "172.16.100.102"}' 'http://localhost:8500/v1/catalog/register' 

curl -XPUT  -H 'Content-Type: application/json' -d '{"Node": "web-node-03", "Datacenter": "qlab01", "NodeMeta": {"somekey": "somevalue"}, "Service": {"Address": "172.16.100.103", "Port": 80, "Service": "web", "Tags": [ "web" ]}, "Address": "172.16.100.103"}' 'http://localhost:8500/v1/catalog/register' 

curl -XPUT  -H 'Content-Type: application/json' -d '{"Node": "db-node-01", "Datacenter": "qlab01", "NodeMeta": {"somekey": "somevalue"}, "Service": {"Address": "172.16.100.105", "Port": 3306, "Service": "db", "Tags": [ "db" ]}, "Address": "172.16.100.105"}' 'http://localhost:8500/v1/catalog/register' 