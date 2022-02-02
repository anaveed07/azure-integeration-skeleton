import Location
import CreateNSG
import CreateSubnet
import CreateIpAdresse
import Config

from client import AzureClient
from createNSG import NetworkSecurity

class NetworkCard:
    def __init__(self):
        self._network_client = AzureClient().network_management_client()


    def create_nic(self, rg_name):
        NIC_NAME = "nic-exemple"
        IP_CONFIG_NAME = "ip-config-exemple"

        poller = self._network_client.network_interfaces.begin_create_or_update(rg_name, NIC_NAME, {
            "location": Location.LOCATION,
            'network_security_group': {
                'id': NetworkSecurity().create_nsg(rg_name).id
            },
            "ip_configurations": [{
                "name" : IP_CONFIG_NAME,
                "subnet" : { "id": CreateSubnet.subnet_result.id},
                "public_ip_address": {"id": CreateIpAdresse.ip_address_result.id}

            }]
        })
        nic_result = poller.result()
        return nic_result