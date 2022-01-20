from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.monitor import MonitorManagementClient
import datetime
from client import AzureClient

# Get a client for Monitor
client = AzureClient().monitor_client()

# Generate query here
today = datetime.datetime.now().date()
filter = "resourceGroupName eq {} and eventTimestamp ge {} and resourceType eq {} ".format('dinCloud-RG01', today, 'Microsoft.Compute/virtualMachines')
select = ",".join([
    "eventTimestamp",
    "eventName",
    "operationName",
    "resourceGroupName",
"resourceType",

])

# Grab activity logs
activity_logs = client.activity_logs.list(
    filter=filter,
    select=select
)

# Print the logs
for log in activity_logs:
    print(" ".join([
        str(log.event_timestamp),
        str(log.resource_group_name),
        log.event_name.localized_value,
        log.resource_type.localized_value.split('/')[1],
        log.operation_name.localized_value.split('/')[2]

    ]))