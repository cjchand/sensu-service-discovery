# Disclaimer

This repo is provided for educational purposes only. This will not be maintained going forward nor is there any support for the code herein, neither by myself nor my employer, T-Mobile.


# Overview

This repo contains the bits used to build a reference implementation for a Service Discovery toolchain using sensu-client to perform the registration on behalf of the app. 

# Usage

1. Clone this repo
2. `cd service-discovery-poc`
3. `docker-compose up`
4. Go to [http://localhost:8500/ui]() to see the Consul UI
5. Go to [http://localhost:3000]() to see the Sensu UI

# How to demo

1. Launch containers, as called out in Usage section above
2. Go to [Sensu UI](http://localhost:3000) and wait a couple of minutes until you see the `get-roles` check on each host in a warning state, reporting that the host is not in Consul
3. Run `seed-consul.sh` script, which puts the hosts into Consul
4. Within a couple of minutes, the `get-roles` check will go green and you will see a `check-http` check added to the web servers
5. Open a new console, cd back into this repo's directory, then type `docker-compose stop web-node-01`
6. Go back to the [Sensu UI](http://localhost:3000) and after a couple of minutes, you will see the `check-http` check for `web-node-01` go into a warning (or, if you wait > 180 seconds critical) state
7. Once you see this, go back to the [Consul UI](http://localhost:8500/ui) and drilldown to the web-node-01 entry where you will see the check show as `failing` in the Consul UI
8. Note, if you refresh the page every 60 seconds or so, you will see the output section change to state `Last check execution was XXX seconds ago`, where `XXX` is the number of seconds since sensu-server last heard a check result for this check
9. Go back to your terminal you opened in Step 5 and type `docker-compose start web-node-01`
10. After about 30-60 seconds, the status in both [Sensu UI](http://localhost:3000) and [Consul UI](http://localhost:8500/ui) will change back to OK/passing


## Auto-addition of subscriptions

When you first launch the containers, the sensu-clients will start reporting in to the sensu-server. There is a check on all web and db servers called `get-role`. The `get-role` check:

1. Queries Consul for the data it knows about this host
2. If the host does not exist in Consul, the `get-role` check goes into a warning state, citing that the host is not in Consul
3. If the host is in Consul, it looks in the Services data for that host and gets the list of tags
4. For each tag it will add a subscription in the sensu-client config, then it restarts sensu-client
5. Once the subscriptions are in place, the sensu-server will push a request to run the appropriate check (web checks, db checks, etc) based on a clients subscriptions

To illustrate this, when you look at the hosts (click `clients`, then any of the clients listed), you will see that they have only one subscription: `client:<client-name>`. This will be interesting in a bit :)

When you run the `seed-consul.sh` script, it will create host entries in Consul for each of the 4 hosts (3x web and 1x db) - including setting tags for each. This is how we get the host to learn its roles and subscribe to the appropriate checks. 

(More coming "soon"....)


# Items left to do:

There are still some things I have to work out:

1. Documentation and tooling around how to add sensu-client configs and Consul services, though there is [some explanation in this preso](https://docs.google.com/presentation/d/1MrVxMbfqwDwSdQv0vh2NmzPt3gD05Mp-OyXkmjoGPAA/edit?usp=sharing) about how the check config and handler work together.


