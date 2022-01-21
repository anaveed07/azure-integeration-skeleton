
from client import AzureClient


location ='EastUS2'
compute_client = AzureClient().compute_client()
instace_types = list(compute_client.virtual_machine_sizes.list(location=location))
instace_types.sort(key=lambda x: (x.number_of_cores, x.memory_in_mb, x.resource_disk_size_in_mb))

print(instace_types)


for li in compute_client.resource_skus.list():
    print(li.resource_type)