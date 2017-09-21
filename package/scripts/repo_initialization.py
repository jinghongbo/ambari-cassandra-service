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

from ambari_commons.os_check import OSCheck

def install_repos():
    import params_repo
  
  #if OSCheck.is_ubuntu_family():
	#cassandra_repo_file = params_repo.repo_ubuntu_path
	#with open(path, "a") as f: 
		#f.write(params_repo.repo_ubuntu_content)
    if OSCheck.is_redhat_family() or OSCheck.is_suse_family():
        with open(params_repo.repo_rhel_suse_path, "w") as f: 
            f.writelines(params_repo.repo_rhel_suse_content)
    else:
        raise Exception('Cassandra repo file path not set for current OS.')
