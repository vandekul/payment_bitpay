# Gateway to Bitpay for Odoo v9.0

## This is the module to connect Odoo 9.0 and Bitpay
This module allow you to create an easily way to accept cryptocurrencies.

## Pre-Configure in your Server
Before installing the module you will need to install this two libraries: <b>bitpay-python-py2</b> and <b>python-ecdsa</b>
    
## Configure Payment Acquirer
* Install BitPay Module -> Website -> eCommerce -> Payment Acquirers -> BitPay
* Put your wanted token. Best option is 'merchant'.
* Put the location as test or live.
* Put and e-mail where you want to receive notifications (optional).
* Put the Confirmation URL where Bitpay will return after payment.
* Check if you want that Odoo send an email to your buyer after transaction is "Confirmed"

![Payment Acquirer](/static/description/PaymentAcquirer.png)

## Transaction Bitpay Details
In transaction object, you will find more technical information about this method of payment:
* Transaction Id: cryptocurrency transaction hash for the executed payout
* Invoice Id: the id of the invoice for which you want to fetch an event token
* Transaction Status: That indicates state of transaction
* Buyer Mail Notification: Indicates if mail has been sent or if not (it will be in blank)

![Transaction Bitpay Details](/static/description/BitpayTxDetails.png)

## Instructions (First time running)
After doing previous steps (Pre-configure your server and Configure Payment Acquirement)
* Open a browser and log in to your bitpay account
* Make an order and try to pay with Bitpay, it will redirect you in order to <a href="https://bitpay.com/api/#rest-api-getting-access" > approve access</a> to bitpay. You only have to Approve it. This step only works once, otherwise you must configure manually or remove token.priv* file
* Log out bitpay account and try to pay again with Bitpay payment method

NOTE: Keep in mind to change API_HOST variable in /controller/merchant_facade.py if you want to check in test enviroment (https://test.bitpay.com) instead of production enviroment (https://bitpay.com)

![Pairing Code](/static/description/bitpay_pairingCode.png)
