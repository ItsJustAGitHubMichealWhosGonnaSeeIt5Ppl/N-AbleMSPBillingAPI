import requests
import logging
from requests import exceptions as req_exc

#TODO add logging
#TODO fix all the generic files that were added
#TODO get version control actually working
#TODO allow different date types to be sent, possibly date range

class MSPBillingAPI:
    def __init__(self, account_id:str, api_key:str):
        """Library for N-Able's MSP Billing API
        
        Version: 0.0.1
        
        Note: This API is still in a limited preview, so things may change!
        
        Finding a contract ID.
            If your invoices are not returning contract IDs, you can also find them in "subscriptionplatform.management".  Click on the desired contract, and the ID will be in the URL.  EG: https://subscriptionplatform.management/subscriptions/contract/<ID HERE>
        
        Official documentation can be found here: https://developer.n-able.com/n-able-cove/reference/post_invoicesready-sfdcid-timeframe-1
        """
        self.session = requests.Session()
        self.acct_id = account_id
        self.url = "https://prod-nableboomi.n-able.com/ws/rest/V1/PSA_API/{endpoint}/" + self.acct_id +"/{variables}"# URL with placeholder for endpoint
        self.session.headers.update({
            'User-Agent': "Python-MSPBillingAPI", # Does not work if using default requests user-agent
            'accept': 'application/json',
            'x-api-key': api_key
            })
    
    def _make_request(self, endpoint:str, variables:list): # Will handle errors and status codes. Variables will be added to the URL in the order they were sent (maybe bad, idk)
        url_variables = "/".join(variables)
        url = self.url.format(endpoint=endpoint, variables=url_variables)
        
        response = self.session.request('post', url=url) # For now there are only post requests
        reason = response.reason
        code = response.status_code
        
        if code == 200: # Success
            return response.json()[endpoint]
        
        elif code == 400: # Bad request
            raise req_exc.RequestException("Error 400: Bad Request.  Make sure your variables are correct.")
        
        elif code == 401: # Bad auth
            raise req_exc.RequestException("Error 401: Unauthorised.  Make sure your account ID and API key are correct.")
        
        elif code == 403: # Comes up with default user-agent
            raise req_exc.RequestException("Error 403: Forbidden.  Your user-agent may be blocked!")
        
        elif code == 404: # Item not found (can appear if variables are wrong)
            raise req_exc.RequestException("Error 404: Not Found.  Make sure your variables are correct.")
        else:
            raise Exception(f"Unknown error: {code}.  Reason: {reason}") 
        
        
    def get_invoices(self, TimeFrame:str):
        """Get invoices for the specified timeframe (single month), including their contract ID.
        
        NOTE: Not all invoices include their contract ID.  I don't know why.  See main docstring for more information.

        Args:
            TimeFrame (str): The billing period in YYYYMM format. Example: '202401'.

        Returns:
            list: List of availabe invoices.
        """
        endpoint = 'InvoicesReady'
        variables = [str(TimeFrame)] # Must be in order! 
        
        return self._make_request(endpoint=endpoint, variables=variables)
        
        
    def get_billable_services(self, TimeFrame:str, ContractId:str):
        """Get billiable services for a contract and timeframe.

        Args:
            TimeFrame (str): The billing period in YYYYMM format. Example: '202401'.
            ContractId (str): Contract ID.  Get this by first requesting your invoices (or see the main docstring).

        Returns:
            list: List of billable services for a contract.
        """
        endpoint = 'PSABillableServices'
        variables = [str(TimeFrame), str(ContractId)] # Must be in order!
        
        return self._make_request(endpoint=endpoint, variables=variables)
        
    
    def get_usage_details(self, TimeFrame:str, ContractId:str, InvoiceId:str):
        """Get usage details for a specific contract and invoice.

        Args:
            TimeFrame (str): The billing period in YYYYMM format. Example: '202401'.
            ContractId (str): Contract ID.  Get this by first requesting your invoices (or see the main docstring).
            InvoiceId (str): Contract ID.  Get this by first requesting your invoices.

        Returns:
            dict: Usage details.
        """
        endpoint = 'PSAUsageDetailsDevices'
        variables = [str(TimeFrame), str(ContractId), str(InvoiceId)] # Must be in order!!
        
        return self._make_request(endpoint=endpoint, variables=variables)