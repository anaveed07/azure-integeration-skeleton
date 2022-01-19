import requests
from client import AzureClient


class Subscription:
    def __init__(self):
        self._clientToken = AzureClient().get_user_access_token()
        #print("login --service-principal --username " + AZURE_CLIENT_ID + " --password " + AZURE_CLIENT_SECRET + " --tenant " + AZURE_TENANT_ID)
        #self._login = az("login --service-principal --username " + AZURE_CLIENT_ID + " --password " + AZURE_CLIENT_SECRET + " --tenant " + AZURE_TENANT_ID)
        #self._login = az("login -u ahsanmalik.7@outlook.com -p " + password)

    def get_billing_info(self):
        url = 'https://management.azure.com/providers/Microsoft.Billing/billingaccounts/?api-version=2020-05-01'
        print(self._clientToken)
        headers = {'Authorization': 'Bearer ' + str(self._clientToken)}
        return requests.get(url, headers=headers)

    def create_new_subscription(self):
       req_body = {
            "properties": {
                'billingScope': '/providers/Microsoft.Billing/BillingAccounts/',
                'DisplayName': 'Dev Team Subscription',
                'Workload': 'Production'
            }
        }



# response = Subscription().get_billing_info()
# l1 = response.json()['value']
# l1 = [y['name'] for y in l1]
# print (l1)