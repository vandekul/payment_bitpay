from bitpay.bitpay_exceptions import *
import bitpay.bitpay_key_utils as bku
from bitpay.bitpay_client import *
import pprint
import logging
import requests
import json
import re
import os.path

# API_HOST = "https://bitpay.com" #for production, live bitcoin
API_HOST = "https://test.bitpay.com"  # for testing, testnet bitcoin
#API_HOST = "https://testnet.demo.btcpayserver.org/" #Testnet BTCPay
KEY_FILE = "/tmp/key.priv"
TOKEN_FILE = "/tmp/token.priv"
_logger = logging.getLogger(__name__)

# check if there is a preexisting key file
if os.path.isfile(KEY_FILE):
    f = open(KEY_FILE, 'r')
    key = f.read()
    f.close()
    _logger.info("Creating a bitpay client using existing private key from disk.")
else:
    key = bku.generate_pem()
    f = open(KEY_FILE, 'w')
    f.write(key)
    f.close()

client = Client(API_HOST, False, key)
pairingCodeURL = ''


def fetch_token(self, facade):
    _logger.info('fetch_token')
    if os.path.isfile(TOKEN_FILE + facade):
        f = open(TOKEN_FILE + facade, 'r')
        token = f.read()
        f.close()
        _logger.info("Reading " + facade + " token from disk.")
        # global client
        #client = Client(API_HOST, False, key, {facade: token})
        client.tokens[facade] = token
        return ''
    else:
        _logger.info("Facade " + facade )
        pairingCode = client.create_token(facade)
        
        pairingCodeURL = API_HOST+"/api-access-request?pairingCode="+pairingCode
        _logger.info("URL PairingCode: %s", pairingCodeURL)

        f = open(TOKEN_FILE + facade, 'w')
        f.write(client.tokens[facade])
        f.close()
        return pairingCodeURL


def get_from_bitpay_api(client, uri, token):
    payload = "?token=%s" % token
    xidentity = bku.get_compressed_public_key_from_pem(client.pem)
    xsignature = bku.sign(uri + payload, client.pem)
    headers = {"content-type": "application/json",
               "X-Identity": xidentity,
               "X-Signature": xsignature, "X-accept-version": "2.0.0"}
    #_logger.info("HEADER %s", headers)
    try:
        # pp.pprint(headers)
        # print(uri + payload)

        response = requests.get(uri + payload, headers=headers, verify=client.verify)
    except Exception as pro:
        raise BitPayConnectionError(pro.args)
    if response.ok:
        #_logger.info("get_from_bitpay_api Response DATA: %s", response.json())
        return response.json()['data']
    client.response_error(response)
"""
POST to any resource
Make sure to include the proper token in the params
"""


def post_to_bitpay_api(client, uri, resource, params):
    payload = json.dumps(params)
    uri = uri + "/" + resource
    xidentity = key_utils.get_compressed_public_key_from_pem(client.pem)
    xsignature = key_utils.sign(uri + payload, client.pem)
    headers = {"content-type": "application/json",
               "accept": "application/json", "X-Identity": xidentity,
               "X-Signature": xsignature, "X-accept-version": "2.0.0"}
    _logger.info("POST_to_bitpay_api uri %s  params %s headers %s", uri, params, headers)
    try:
        
        response = requests.post(uri, data=payload, headers=headers, verify=client.verify)
        _logger.info("Response %s", response)
    except Exception as pro:
        raise BitPayConnectionError(pro.args)
    if response.ok:
        return response.json()['data']
        #return response.decode(json.detect_encoding(response))
    client.response_error(response)


# pp = pprint.PrettyPrinter(indent=4)
