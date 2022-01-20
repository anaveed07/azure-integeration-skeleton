from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from conf import AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, AZURE_SUBSCRIPTION_ID
from az.cli import az
import adal


class ClientLocator:
    def __init__(self, client):
        self._login = ''
        self._credentials = DefaultAzureCredential()

        self._subscription_id = None
        self._subscription_client = None
        self._resource_client = None
        self._compute_client = None
        self._access_token = None
        self._network_management_client = None
        self._monitor_client = None

    def subscription_client(self):
        if not self._subscription_client:
            self._subscription_client = SubscriptionClient(self._credentials)
        return self._subscription_client

    def subscription_id(self):
        subscription = next(self.subscription_client().subscriptions.list())
        self._subscription_id = subscription.subscription_id
        return self._subscription_id

    def resource_client(self):
        if not self._resource_client:
            self._resource_client = ResourceManagementClient(self._credentials, self.subscription_id())
        return self._resource_client

    def compute_client(self):
        if not self._compute_client:
            self._compute_client = ComputeManagementClient(self._credentials, self.subscription_id())
        return self._compute_client

    def network_management_client(self):
        if not self._network_management_client:
            self._network_management_client = NetworkManagementClient(self._credentials, Az)
        return self._network_management_client

    def monitor_client(self):
        if not self._monitor_client:
            self._monitor_client = MonitorManagementClient(self._credentials, self.subscription_id())

        return self._monitor_client


    def get_user_access_token(self):
        #print(f"login -u {conf.USER_NAME} -p {conf.USER_PASS}")
        #self._login = az(f"login -u {conf.USER_NAME} -p {conf.USER_PASS}")
        #print(self._login)
        user_token = az("account get-access-token").result_dict['accessToken']
        return user_token

    def get_sp_access_token(self):
        authentication_endpoint = 'https://login.microsoftonline.com/'
        resource = 'https://management.core.windows.net/'  # get an Azure access token using the adal library
        context = adal.AuthenticationContext(authentication_endpoint + AZURE_TENANT_ID)
        token_response = context.acquire_token_with_client_credentials(resource, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
        self._access_token = token_response.get('accessToken')
        return "Bearer " + self._access_token


class AzureClient(ClientLocator):
    def __init__(self):
        super().__init__('azure')




# client = AzureClient().get_subscription_client()
# subscription = next(_.subscriptions.list())
# #subs = [sub.as_dict() for sub in subscription]
# print(subscription.display_name)
#
# print (AzureClient().get_access_token())