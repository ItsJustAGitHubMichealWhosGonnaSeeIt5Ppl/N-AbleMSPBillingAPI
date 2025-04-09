# N-Able MSP Billing API wrapper
Wrapper for N-Able's new MSP Billing API

Official documentation: https://developer.n-able.com/n-able-cove/reference/post_invoicesready-sfdcid-timeframe-1

How to get access: https://developer.n-able.com/n-able-cove/docs/billing

## Installation
TBD
```

```

## Getting Started
```
import MSPBillingAPI
import os

ACCOUNT = os.getenv("ACCOUNT")
API_KEY = os.getenv("API_KEY")



api = MSPBillingAPI.MSPBillingAPI(ACCOUNT, API_KEY)
my_latest_invoice = api.get_invoices("202503")
```

# Quirks
Since this API is still in early preview, it has some quirks (also known as issues)

## Contract IDs
For some reason, not all invoices return their contract (and ID), which makes this API somewhat useless. Luckily, you can get a contract ID from "subscriptionplatform.management".  

To get the ID, click on the desired contract, and the ID will be in the URL.  E.g: `https://subscriptionplatform.management/subscriptions/contract/[ID HERE]` 
This ID can then be used for calls.

Don't be fooled by the "Contract ID" label on the sidebar (format: MSP-[Some Numbers]).  The API refers to that as your "Contract Number".

## Invoice IDs
While you shouldn't need to, invoice IDs can be found here: https://subscriptionplatform.management/subscriptions/dashboard/invoices.