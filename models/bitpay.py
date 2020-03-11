# -*- coding: utf-8 -*-
##############################################################################
#
#    ZamTech
#    Copyright (C) 2018-Today ZamTech (http://www.zamte.com/)
#
##############################################################################

#from odoo import fields, models, api
from openerp import api, fields, models, _
from openerp.osv import osv
import ecdsa
from ..controller.main import BitpayController
from ..controller import merchant_facade
from werkzeug import urls
import json, ast

import logging
import pprint

from openerp import http, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class AcquirerBitPay(models.Model):
    _inherit = 'payment.acquirer'

    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerBitPay, self)._get_providers(cr, uid, context=context)
        providers.append(['bitpay', 'bitpay'])
        return providers

    token = fields.Char('Token', help='Token type: merchant/pos/payroll')  #merchant
    location = fields.Char('Location', size=64) 
    notificationEmail = fields.Char('Notifications Email from Bitpay', help=' Notifications email in your company, if it is empty no notifications will be send')
    confirmationURL = fields.Char('Confirmation URL', help='Confirmation URL to return after Bitpay payment')
    buyerNotification = fields.Boolean('Odoo confirmation mail to buyer', help='If it is checked, Odoo will send the confirmation mail defined')

    _defaults = {
        'token': 'merchant',
        'location':'https://test.bitpay.com/', #Testnet BitPay
        #'location':'https://testnet.demo.btcpayserver.org/', #Testnet BTCPay
        'notificationEmail':'susanna@zynthian.org',
        'confirmationURL':'http://odoo-dev.zynthian.org/shop/confirmation',
        'buyerNotification': 'True',
    }

class BitPayTransaction(models.Model):
    _inherit = "payment.transaction"
    bitpay_invoiceId = fields.Char("Invoice Id")
    bitpay_txid = fields.Char("Transaction Id")
    bitpay_status = fields.Char("Transaction Status")
    bitpay_buyerMailNotification = fields.Char("Buyer Mail Notification")
    acquirer_name = fields.Selection(related='acquirer_id.provider')