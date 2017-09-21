#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
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

from resource_management import *
from properties_config import properties_config
import sys
import os
from copy import deepcopy

def getDirectoriesToCreate( dirs ):
    "This checks if exists the intermediate directories"
    output = []
    for dir in dirs:
        folders = dir.split('/')
        tmpFolder = ''
        for folder in folders[1:]:
            tmpFolder += '/' + folder
            if not os.path.isdir(tmpFolder):
                output.append(tmpFolder)
        output.append(dir)
    return output
	
def cassandra():
    import params_dirs
	
    Directory([params_dirs.log_dir, params_dirs.pid_dir, params_dirs.conf_dir],
              owner=params_dirs.cassandra_user,
              group=params_dirs.user_group
          )
	
	# Parametros intermedios para convertir en data_file_directories
	# master_nodes_ips					<-- 'none' or comma separated values
	# master_data_file_directories		<-- comma separated values directories for store data on the master(s)
	# slave_data_file_directories		<-- comma separated values directories for store data on the slave(s) 
	
	# Aqui va el directorio bueno bueno, por defecto el de los slaves (el mas probable)
    dirs = params_dirs.slave_data_file_directories.split(',')
	
    if params_dirs.master_nodes_ips != 'none':
        mni = params_dirs.master_nodes_ips.split(',')
        if params_dirs.listen_address in mni:
            dirs = params_dirs.master_data_file_directories.split(',')
			
    Directory(getDirectoriesToCreate(dirs), owner=params_dirs.cassandra_user, group=params_dirs.user_group)

    File(format("{conf_dir}/cassandra.yaml"),
        content=Template(
        "cassandra.master.yaml.j2", 
        configurations = params_dirs),
        owner=params_dirs.cassandra_user,
        group=params_dirs.user_group 
    )
