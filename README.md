# ambari-cassandra-service
Ambari service for installing and managing Cassandra on HDP clusters. Apache Cassandra is an open source distributed database management system designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure.

Author: [Amey Jain](https://github.com/ajak6)

#### Setup
- Download HDP 2.3 sandbox VM image (Sandbox_HDP_2.3_1_VMware.ova) from [Hortonworks website](http://hortonworks.com/products/hortonworks-sandbox/)
- Import Sandbox_HDP_2.3_1_VMware.ova into VMWare and set the VM memory size to 8GB
- Now start the VM
- After it boots up, find the IP address of the VM and add an entry into your machines hosts file. For example:
```
xx.xx.xx.xx sandbox.hortonworks.com sandbox    
```
  - Note that you will need to replace the above xx.xx.xx.xx with the IP for your own VM
  
- Connect to the VM via SSH (password hadoop)
```
ssh root@sandbox.hortonworks.com
```

- To download the Cassandra service folder, run below
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/Dominion-Digital/ambari-cassandra-service.git   /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/CASSANDRA   
```
- Restart Ambari
```
#sandbox
service ambari restart

#non sandbox
sudo service ambari-server restart
```

- Then you can click on 'Add Service' from the 'Actions' dropdown menu in the bottom left of the Ambari dashboard:

On bottom left -> Actions -> Add service -> check Cassandra -> Next -> check nodes to be present in the cluster and act as client-> Next -> Change any config you like (e.g. install dir, memory sizes, num containers or values in cassandra.yaml) -> Next -> Deploy
Add the Ip address of all the seed nodes in the ring. It can be 1 to many. Add comma separated IP/Hostname value in quotes.

If you want to specify a different path for data directories on master node and slaves nodes change this parameters.
- master_nodes_ips ('none' if all nodes must have the same config (slave_data_file_directories will be used), comma separated values instead.)
- master_data_file_directories [comma separated values]
- slave_data_file_directories [comma separated values]

 ![Image](../master/screenshots/Initial-config.png?raw=true)

- On successful deployment you will see the Cassandra service as part of Ambari stack and will be able to start/stop the service from here:
 ![Image](../master/screenshots/Installed-service-stop.png?raw=true)

- You can see the parameters you configured under 'Configs' tab
![Image](../master/screenshots/Installed-service-config.png?raw=true)


#### Remove service

- To remove the Cassandra service: 
  - Stop the service via Ambari
  - Unregister the service

  ```
export SERVICE=Cassandra
export PASSWORD=admin
export AMBARI_HOST=localhost
#detect name of cluster
output=`curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari'  http://$AMBARI_HOST:8080/api/v1/clusters`
CLUSTER=`echo $output | sed -n 's/.*"cluster_name" : "\([^\"]*\)".*/\1/p'`

curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X DELETE http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#if above errors out, run below first to fully stop the service
#curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE
  ```
  - Remove artifacts
  ```
  rm -rf /var/lib/cassandra/*
  
  #on ambari server
  
  rm -rf /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/CASSANDRA
  
  #on all nodes
  
  rm -rf /var/lib/ambari-agent/cache/stacks/HDP/$VERSION/services/CASSANDRA
  
  yum erase cassandra -y
  
  ```
  - Clean ambari database configuration for cassandra service, else ambari will warn on every start.
  https://discuss.pivotal.io/hc/en-us/articles/217649658-How-to-connect-to-Ambari-s-PostgreSQL-database-
  ```
  #Determine the process ID for the Ambari postgres instance
  
  ps -eaf | grep ambari | grep postgres | awk '{print $3}'
  
  #Determine the port that is being used by the Ambari PostgreSQL instance by using the process ID found previously
  
  netstat -anp | grep 2855
  
  #Log on to the Ambari database with the command below (default password is 'bigdata')
  
  psql ambari -U ambari -W -p 5432
  
  #Find cassandra configurations
  
  select config_id, version_tag, version, type_name from clusterconfig c where c.type_name LIKE '%cassandra%';
  
  #Delete rows
  
  delete from clusterconfig c where c.type_name LIKE '%cassandra%';
  
  #Exit postgres console
  
  \q
  
  ```   
  
# License
Copyright 2017 DOMINION.

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
