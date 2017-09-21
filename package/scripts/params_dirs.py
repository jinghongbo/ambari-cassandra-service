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

def getPrettyDataDirectories( str ):
	"This builds a string for the yaml file"
	outputStr = ''
	dirs = str.split(',')
	for dir in dirs:
		outputStr += '    - ' + dir + '\r\n'

	return outputStr

# server configurations
config = Script.get_config()

cassandra_home = '/etc/cassandra/'
cassandra_bin = '/usr/sbin/cassandra'
cassandra_pid_dir = config['configurations']['cassandra-env']['cassandra_pid_dir']
cassandra_pid_file = format("{cassandra_pid_dir}/cassandra.pid")

conf_dir = "/etc/cassandra/conf"
cassandra_user = config['configurations']['cassandra-env']['cassandra_user']
log_dir = config['configurations']['cassandra-env']['cassandra_log_dir']
pid_dir = '/var/run/cassandra'
pid_file = '/var/run/cassandra/cassandra.pid'

hostname = config['hostname']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['hostLevelParams']['java_home']

template = config['configurations']['cassandra-site']['template']
defaultName = config['configurations']['cassandra-site']['defaultName']

# Para poder configurar diferentes carpetas dependiendo de si es el master o un slave
# data_file_directories=config['configurations']['cassandra-site']['data_file_directories']
master_nodes_ips=config['configurations']['cassandra-site']['master_nodes_ips']
master_data_file_directories=config['configurations']['cassandra-site']['master_data_file_directories']
slave_data_file_directories=config['configurations']['cassandra-site']['slave_data_file_directories']

# a,listen_address1=commands.getstatusoutput('hostname -i')
#listen_address=config['configurations']['cassandra-site']['listen_address1']
#listen_address=commands.getstatusoutput("hostname -i | awk '{print $NF}'")
a,listen_address=commands.getstatusoutput("hostname -i | awk '{print $NF}'")
# Use emtpy listen address but the host's broadcast_rpc_address
#listen_address=''
start_native_transport=config['configurations']['cassandra-site']['start_native_transport']
native_transport_port=config['configurations']['cassandra-site']['native_transport_port']
start_rpc=config['configurations']['cassandra-site']['start_rpc']

# Parametros intermedios para convertir en data_file_directories
# master_nodes_ips					<-- 'none' or comma separated values
# master_data_file_directories		<-- comma separated values directories for store data on the master(s)
# slave_data_file_directories		<-- comma separated values directories for store data on the slave(s) 

# Aqui va el directorio bueno bueno, por defecto el de los slaves (el mas probable)
data_file_directories_py = getPrettyDataDirectories( slave_data_file_directories )

if master_nodes_ips != 'none':
	mni = master_nodes_ips.split(',')
	if listen_address in mni:
		data_file_directories_py = getPrettyDataDirectories( master_data_file_directories )

hints_directory=config['configurations']['cassandra-site']['hints_directory']
commitlog_directory=config['configurations']['cassandra-site']['commitlog_directory']
saved_caches_directory=config['configurations']['cassandra-site']['saved_caches_directory']

# cassandra-site
cluster_name_py = config['configurations']['cassandra-site']['cluster_name']
seed_provider_parameters_seeds = config['configurations']['cassandra-site']['seed_provider_parameters_seeds']
hinted_handoff_throttle_in_kb=config['configurations']['cassandra-site']['hinted_handoff_throttle_in_kb']
max_hints_delivery_threads=config['configurations']['cassandra-site']['max_hints_delivery_threads']
hints_flush_period_in_ms=config['configurations']['cassandra-site']['hints_flush_period_in_ms']
max_hints_file_size_in_mb=config['configurations']['cassandra-site']['max_hints_file_size_in_mb']
num_tokens=config['configurations']['cassandra-site']['num_tokens']
hinted_handoff_enabled=config['configurations']['cassandra-site']['hinted_handoff_enabled']
max_hint_window_in_ms=config['configurations']['cassandra-site']['max_hint_window_in_ms']
batchlog_replay_throttle_in_kb=config['configurations']['cassandra-site']['batchlog_replay_throttle_in_kb']
authenticator=config['configurations']['cassandra-site']['authenticator']
authorizer=config['configurations']['cassandra-site']['authorizer']
role_manager=config['configurations']['cassandra-site']['role_manager']
roles_validity_in_ms=config['configurations']['cassandra-site']['roles_validity_in_ms']
permissions_validity_in_ms=config['configurations']['cassandra-site']['permissions_validity_in_ms']
credentials_validity_in_ms=config['configurations']['cassandra-site']['credentials_validity_in_ms']
partitioner=config['configurations']['cassandra-site']['partitioner']
cdc_enabled=config['configurations']['cassandra-site']['cdc_enabled']
disk_failure_policy=config['configurations']['cassandra-site']['disk_failure_policy']
commit_failure_policy=config['configurations']['cassandra-site']['commit_failure_policy']
prepared_statements_cache_size_mb=config['configurations']['cassandra-site']['prepared_statements_cache_size_mb']
thrift_prepared_statements_cache_size_mb=config['configurations']['cassandra-site']['thrift_prepared_statements_cache_size_mb']
key_cache_size_in_mb=config['configurations']['cassandra-site']['key_cache_size_in_mb']
key_cache_save_period=config['configurations']['cassandra-site']['key_cache_save_period']
row_cache_size_in_mb=config['configurations']['cassandra-site']['row_cache_size_in_mb']
row_cache_save_period=config['configurations']['cassandra-site']['row_cache_save_period']

counter_cache_save_period=config['configurations']['cassandra-site']['counter_cache_save_period']
commitlog_sync=config['configurations']['cassandra-site']['commitlog_sync']
commitlog_sync_period_in_ms=config['configurations']['cassandra-site']['commitlog_sync_period_in_ms']
commitlog_segment_size_in_mb=config['configurations']['cassandra-site']['commitlog_segment_size_in_mb']
concurrent_reads=config['configurations']['cassandra-site']['concurrent_reads']
concurrent_writes=config['configurations']['cassandra-site']['concurrent_writes']
concurrent_counter_writes=config['configurations']['cassandra-site']['concurrent_counter_writes']
concurrent_materialized_view_writes=config['configurations']['cassandra-site']['concurrent_materialized_view_writes']
memtable_allocation_type=config['configurations']['cassandra-site']['memtable_allocation_type']
index_summary_capacity_in_mb=config['configurations']['cassandra-site']['index_summary_capacity_in_mb']
index_summary_resize_interval_in_minutes=config['configurations']['cassandra-site']['index_summary_resize_interval_in_minutes']
trickle_fsync=config['configurations']['cassandra-site']['trickle_fsync']
trickle_fsync_interval_in_kb=config['configurations']['cassandra-site']['trickle_fsync_interval_in_kb']
storage_port=config['configurations']['cassandra-site']['storage_port']
ssl_storage_port=config['configurations']['cassandra-site']['ssl_storage_port']

rpc_address=config['configurations']['cassandra-site']['rpc_address1']
rpc_port=config['configurations']['cassandra-site']['rpc_port']
#broadcast_rpc_address=config['configurations']['cassandra-site']['broadcast_rpc_address']
a,broadcast_rpc_address=commands.getstatusoutput("hostname -i | awk '{print $NF}'")
rpc_keepalive=config['configurations']['cassandra-site']['rpc_keepalive']
rpc_server_type=config['configurations']['cassandra-site']['rpc_server_type']
thrift_framed_transport_size_in_mb=config['configurations']['cassandra-site']['thrift_framed_transport_size_in_mb']


incremental_backups = config['configurations']['cassandra-site']['incremental_backups']
snapshot_before_compaction = config['configurations']['cassandra-site']['snapshot_before_compaction']
auto_snapshot = config['configurations']['cassandra-site']['auto_snapshot']
tombstone_warn_threshold = config['configurations']['cassandra-site']['tombstone_warn_threshold']
tombstone_failure_threshold = config['configurations']['cassandra-site']['tombstone_failure_threshold']
column_index_size_in_kb = config['configurations']['cassandra-site']['column_index_size_in_kb']
column_index_cache_size_in_kb = config['configurations']['cassandra-site']['column_index_cache_size_in_kb']
batch_size_warn_threshold_in_kb = config['configurations']['cassandra-site']['batch_size_warn_threshold_in_kb']
compaction_throughput_mb_per_sec = config['configurations']['cassandra-site']['compaction_throughput_mb_per_sec']
compaction_large_partition_warning_threshold_mb = config['configurations']['cassandra-site']['compaction_large_partition_warning_threshold_mb']
sstable_preemptive_open_interval_in_mb = config['configurations']['cassandra-site']['sstable_preemptive_open_interval_in_mb']
read_request_timeout_in_ms = config['configurations']['cassandra-site']['read_request_timeout_in_ms']
range_request_timeout_in_ms = config['configurations']['cassandra-site']['range_request_timeout_in_ms']
write_request_timeout_in_ms = config['configurations']['cassandra-site']['write_request_timeout_in_ms']
counter_write_request_timeout_in_ms = config['configurations']['cassandra-site']['counter_write_request_timeout_in_ms']
cas_contention_timeout_in_ms = config['configurations']['cassandra-site']['cas_contention_timeout_in_ms']
truncate_request_timeout_in_ms = config['configurations']['cassandra-site']['truncate_request_timeout_in_ms']
request_timeout_in_ms = config['configurations']['cassandra-site']['request_timeout_in_ms']
slow_query_log_timeout_in_ms = config['configurations']['cassandra-site']['slow_query_log_timeout_in_ms']
cross_node_timeout = config['configurations']['cassandra-site']['cross_node_timeout']
endpoint_snitch = config['configurations']['cassandra-site']['endpoint_snitch']
dynamic_snitch_update_interval_in_ms = config['configurations']['cassandra-site']['dynamic_snitch_update_interval_in_ms']
dynamic_snitch_reset_interval_in_ms = config['configurations']['cassandra-site']['dynamic_snitch_reset_interval_in_ms']
dynamic_snitch_badness_threshold = config['configurations']['cassandra-site']['dynamic_snitch_badness_threshold']
request_scheduler = config['configurations']['cassandra-site']['request_scheduler']

server_encryption_options_internode_encryption = config['configurations']['cassandra-site']['server_encryption_options_internode_encryption']
server_encryption_options_keystore = config['configurations']['cassandra-site']['server_encryption_options_keystore']
server_encryption_options_keystore_password = config['configurations']['cassandra-site']['server_encryption_options_keystore_password']
server_encryption_options_truststore = config['configurations']['cassandra-site']['server_encryption_options_truststore']
server_encryption_options_truststore_password = config['configurations']['cassandra-site']['server_encryption_options_truststore_password']

client_encryption_options_enabled=config['configurations']['cassandra-site']['client_encryption_options_enabled']
client_encryption_options_keystore_password = config['configurations']['cassandra-site']['client_encryption_options_keystore_password']
client_encryption_options_keystore = config['configurations']['cassandra-site']['client_encryption_options_keystore']

internode_compression = config['configurations']['cassandra-site']['internode_compression']
inter_dc_tcp_nodelay = config['configurations']['cassandra-site']['inter_dc_tcp_nodelay']
key_cache_size_in_mb = config['configurations']['cassandra-site']['key_cache_size_in_mb']
counter_cache_size_in_mb = config['configurations']['cassandra-site']['counter_cache_size_in_mb']
seed_provider_class_name = config['configurations']['cassandra-site']['seed_provider_class_name']
seed_provider_parameters_seeds = config['configurations']['cassandra-site']['seed_provider_parameters_seeds']
index_summary_capacity_in_mb = config['configurations']['cassandra-site']['index_summary_capacity_in_mb']

inter_dc_tcp_nodelay= config['configurations']['cassandra-site']['inter_dc_tcp_nodelay']
tracetype_query_ttl= config['configurations']['cassandra-site']['tracetype_query_ttl']
tracetype_repair_ttl= config['configurations']['cassandra-site']['tracetype_repair_ttl']
enable_user_defined_functions= config['configurations']['cassandra-site']['enable_user_defined_functions']
enable_scripted_user_defined_functions= config['configurations']['cassandra-site']['enable_scripted_user_defined_functions']
tdeo_enabled= config['configurations']['cassandra-site']['tdeo_enabled']
tdeo_chunk_length_kb= config['configurations']['cassandra-site']['tdeo_chunk_length_kb']
tdeo_cipher= config['configurations']['cassandra-site']['tdeo_cipher']
tdeo_key_alias_testing= config['configurations']['cassandra-site']['tdeo_key_alias_testing']
tdeo_class_name= config['configurations']['cassandra-site']['tdeo_class_name']
tdeo_keystore= config['configurations']['cassandra-site']['tdeo_keystore']
tdeo_keystore_password= config['configurations']['cassandra-site']['tdeo_keystore_password']
tdeo_store_type= config['configurations']['cassandra-site']['tdeo_store_type']
tdeo_key_password= config['configurations']['cassandra-site']['tdeo_key_password']
batch_size_fail_threshold_in_kb= config['configurations']['cassandra-site']['batch_size_fail_threshold_in_kb']
unlogged_batch_across_partitions_warn_threshold= config['configurations']['cassandra-site']['unlogged_batch_across_partitions_warn_threshold']
gc_warn_threshold_in_ms= config['configurations']['cassandra-site']['gc_warn_threshold_in_ms']
back_pressure_enabled= config['configurations']['cassandra-site']['back_pressure_enabled']
back_pressure_strategy_class_name= config['configurations']['cassandra-site']['back_pressure_strategy_class_name']
back_pressure_strategy_parameters_high_ratio= config['configurations']['cassandra-site']['back_pressure_strategy_parameters_high_ratio']
back_pressure_strategy_parameters_factor= config['configurations']['cassandra-site']['back_pressure_strategy_parameters_factor']
back_pressure_strategy_parameters_flow= config['configurations']['cassandra-site']['back_pressure_strategy_parameters_flow']
auto_bootstrap= config['configurations']['cassandra-site']['auto_bootstrap']
windows_timer_interval= config['configurations']['cassandra-site']['windows_timer_interval']

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