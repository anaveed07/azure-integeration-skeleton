from client import AzureClient
from msrestazure.azure_exceptions import CloudError


class DefaultSettings():
    resource_group = 'aztk'
    storage_account = 'aztkstorage'
    batch_account = 'aztkbatch'
    virtual_network_name = "aztkvnet"
    subnet_name = 'aztksubnet'
    application_name = 'aztkapplication'
    application_credential_name = 'aztkapplicationcredential'
    service_principal = 'aztksp'
    region = 'westus'


class AccountSetupError(Exception):
    pass


class ResourceGroup:
    def __init__(self):
        self._resource_client = AzureClient().resource_client()

    def create_resource_group(self, **kwargs):
        """
            Create a resource group
            :param **resource_group: str
            :param **region: str
        """

        self._resource_client.resource_groups.list()

        for i in range(3):
            try:
                resource_group = self._resource_client.resource_groups.create_or_update(
                    resource_group_name=kwargs.get("resource_group", DefaultSettings.resource_group),
                    parameters={
                        'location': kwargs.get("region", DefaultSettings.region),
                    })
            except CloudError as e:
                if i == 2:
                    raise AccountSetupError("Unable to create resource group in region {}".format(
                        kwargs.get("region", DefaultSettings.region)))
                print(e.message)
                print("Please try again.")
                kwargs["resource_group"] = self.prompt_with_default("Azure Region", DefaultSettings.region)
        return resource_group.id

    def list_resource_groups(self):
        # List Resource Groups
        print("List Resource Groups")
        for item in self._resource_client.resource_groups.list():
            self.print_item(item)

    def delete_resource_group(self, group_name):
        print("Delete Resource Group")
        if group_name in self._resource_client.resource_groups.list():
            delete_async_operation = self._resource_client.resource_groups.begin_delete(group_name)
            delete_async_operation.wait()
        else:
            print("No resource group found")
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

    @staticmethod
    def prompt_with_default(key, value):
        user_value = input("{0} [{1}]: ".format(key, value))
        if user_value != "":
            return user_value
        else:
            return value

ResourceGroup().create_resource_group(resource_group='ahsan-test')