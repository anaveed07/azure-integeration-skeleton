from client import AzureClient
from  createNIC import NetworkCard
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network.models import NetworkSecurityGroup
from azure.mgmt.network.models import SecurityRule


NSG_NAME = "nsg-exemple"


class NetworkSecurity:
    def __init__(self):
        self._nsg_client = AzureClient().network_management_client()

    def create_nsg(self, rg_name):
        parameters = NetworkSecurityGroup()
        parameters.security_rules = [SecurityRule(
            protocol='Tcp',
            access='Allow',
            direction='Inbound',
            description='Allow RDP port 3389',
            source_address_prefix='*',
            destination_address_prefix='*',
            source_port_range='*',
            destination_port_range='3389',
            priority=100,
            name='RDP1')]
        poller = self._nsg_client.network_security_groups.begin_create_or_update(rg_name, NSG_NAME,
                                                                                 parameters)

        nsg_result = poller.result()
        return nsg_result

    def delete_nsg(self, rg_name, nsg_name):
        try:
            self._nsg_client.network_security_groups.delete(
                resource_group_name=rg_name,
                network_security_group_name=nsg_name,
            )
        except CloudError as e:
            return "FAILURE", "Network security group could not be deleted", ""

        return "SUCCESS", "The network security group has been succesfully deleted", ""
