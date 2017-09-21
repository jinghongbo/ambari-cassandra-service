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

seed_provider_parameters_seeds = config['configurations']['cassandra-site']['seed_provider_parameters_seeds']
native_transport_port=config['configurations']['cassandra-site']['native_transport_port']
