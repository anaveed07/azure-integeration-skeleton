import datetime
from azure.mgmt.monitor import MonitorManagementClient
from client import AzureClient
# Get the ARM id of your resource. You might chose to do a "get"
# using the according management or to build the URL directly
# Example for a ARM VM
today = datetime.datetime.utcnow()
nexttime = today - datetime.timedelta(minutes=5)

query_timespan = "{}/{}".format(nexttime, today - datetime.timedelta(minutes=4))

print(query_timespan)

resource_group_name = "dinCloud-RG01"
vm_name = "ExampleVM"
subscription_id = "517ba743-f3f4-4e21-9f1c-99dfcdb3508c"
resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(subscription_id, resource_group_name, vm_name)

# create client
client = AzureClient().monitor_client()

# You can get the available metrics of this specific resource
for metric in client.metric_definitions.list(resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))

metrics_data = client.metrics.list(
    resource_id,
    timespan=query_timespan,
    interval='PT1M',
    metricnames='Percentage CPU',
    aggregation='average'
)
for item in metrics_data.value:
    for timeserie in item.timeseries:
        for data in timeserie.data:
            print("{}".format(data.average))

# Example of result for a VM:
# Percentage CPU: id=Percentage CPU, unit=Unit.percent
# Network In: id=Network In, unit=Unit.bytes
# Network Out: id=Network Out, unit=Unit.bytes
# Disk Read Bytes: id=Disk Read Bytes, unit=Unit.bytes
# Disk Write Bytes: id=Disk Write Bytes, unit=Unit.bytes
# Disk Read Operations/Sec: id=Disk Read Operations/Sec, unit=Unit.count_per_second
# Disk Write Operations/Sec: id=Disk Write Operations/Sec, unit=Unit.count_per_second

# Get CPU total of yesterday for this VM, by hour

today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(days=1)

metrics_data = client.metrics.list(
    resource_id,
    timespan="{}/{}".format(yesterday, today),
    interval='PT1H',
    metricnames='Percentage CPU',
    aggregation='Total'
)

for item in metrics_data.value:
    # azure.mgmt.monitor.models.Metric
    #print("{} ({})".format(item.unit.name.localized_value, item.unit.name))
    for timeserie in item.timeseries:
        for data in timeserie.data:
            # azure.mgmt.monitor.models.MetricData

            print("{}: {}".format(data.time_stamp, data.total))