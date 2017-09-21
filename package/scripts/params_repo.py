#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from resource_management.libraries.functions.version import format_stack_version, compare_versions
from resource_management import *
import commands

# server configurations
config = Script.get_config()

# repo templates
# repo_rhel_suse =  config['configurations']['cluster-env']['repo_suse_rhel_template']
# repo_ubuntu =  config['configurations']['cluster-env']['repo_ubuntu_template']

repo_rhel_suse_path = "/etc/yum.repos.d/cassandra.repo"
repo_ubuntu_path = "/etc/apt/sources.list.d/cassandra.sources.list"

repo_rhel_suse_content = 	["[cassandra]\n",
							"name=Apache Cassandra\n",
							"baseurl=https://www.apache.org/dist/cassandra/redhat/311x/\n",
							"gpgcheck=1\n",
							"repo_gpgcheck=1\n",
							"gpgkey=https://www.apache.org/dist/cassandra/KEYS"]

repo_ubuntu_content = "deb http://www.apache.org/dist/cassandra/debian 311x main"

"""
Installation from Debian packages
	For the <release series> specify the major version number, without dot, and with an appended x.
	The latest <release series> is 311x.
	For older releases, the <release series> can be one of 30x, 22x, or 21x.

	Add the Apache repository of Cassandra to /etc/apt/sources.list.d/cassandra.sources.list, for example for the latest 3.11 version:
		echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
	Add the Apache Cassandra repository keys:
		curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
	Update the repositories:
		sudo apt-get update
	If you encounter this error:
		GPG error: http://www.apache.org 311x InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY A278B781FE4B2BDA
	Then add the public key A278B781FE4B2BDA as follows:
		sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-key A278B781FE4B2BDA
	and repeat sudo apt-get update. The actual key may be different, you get it from the error message itself. For a full list of Apache contributors public keys, you can refer to https://www.apache.org/dist/cassandra/KEYS.
	Install Cassandra:
		sudo apt-get install cassandra
	You can start Cassandra with sudo service cassandra start and stop it with sudo service cassandra stop. However, normally the service will start automatically. For this reason be sure to stop it if you need to make any configuration changes.
	Verify that Cassandra is running by invoking nodetool status from the command line.
	The default location of configuration files is /etc/cassandra.
	The default location of log and data directories is /var/log/cassandra/ and /var/lib/cassandra.
	Start-up options (heap size, etc) can be configured in /etc/default/cassandra.
"""