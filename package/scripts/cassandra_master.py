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

from resource_management import *
import signal
import sys
import os
from os.path import isfile

from cassandra import cassandra
from shared_initialization import *
from repo_initialization import *


class Cassandra_Master(Script):
    def install(self, env):
        import params
        env.set_params(params)
        print 'Install'
        # Before installing we must add the repo file
        install_repos()
        install_packages()
        self.install_packages(env)
    def configure(self, env):
        import params_dirs
        env.set_params(params_dirs)
        print 'Install plugins'
        cassandra()
    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        print 'Stop the Master'
        cmd = format("service cassandra stop")
        Execute(cmd)
    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        print 'Start the Master'
        cmd = format("service cassandra start")
        Execute(cmd)
    def status(self, env):
        import params
        env.set_params(params)
        print 'Status of the Master'
        controller_pid = "/var/run/cassandra/cassandra.pid"
        check_process_status(controller_pid)
    
if __name__ == "__main__":
    Cassandra_Master().execute()
