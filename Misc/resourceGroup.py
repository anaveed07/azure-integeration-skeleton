from client import AzureClient


class ResourceGroup:
    def __init__(self):
        self._client = AzureClient().get_resrcmgmt_client()

    def create_resource_group(self,group_name, resource_group_params={"location": "westus"}):
        print("create new resource group")

        self._client.resource_groups.create_or_update(group_name, resource_group_params)

    def list_resource_groups(self):
        # List Resource Groups
        print("List Resource Groups")
        for item in self._client.resource_groups.list():
            self.print_item(item)

    def delete_resource_group(self, group_name):
        print("Delete Resource Group")
        delete_async_operation = self._client.resource_groups.begin_delete(group_name)
        delete_async_operation.wait()
        print("\nDeleted: {}".format(group_name))

    def print_item(self, group):
        """Print a ResourceGroup instance."""
        print("\tName: {}".format(group.name))
        print("\tId: {}".format(group.id))
        print("\tLocation: {}".format(group.location))
        print("\tTags: {}".format(group.tags))
        self.print_properties(group.properties)

    @staticmethod
    def print_properties(props):
        """Print a ResourceGroup properties instance."""
        if props and props.provisioning_state:
            print("\tProperties:")
            print("\t\tProvisioning State: {}".format(props.provisioning_state))
        print("\n\n")




ResourceGroup().create_resource_group('azure-test-group-py')