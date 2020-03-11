# -*- coding: utf-8 -*-

import json
import logging
import pprint

import requests
import werkzeug
import merchant_facade
import bitpay.bitpay_key_utils as bku
import urllib2,cookielib

from openerp import api, fields, models, _
from openerp.osv import osv

from openerp import http, SUPERUSER_ID
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.http import request


_logger = logging.getLogger(__name__)


class BitpayController(http.Controller):
    _notify_url = '/payment/bitpay/ipn'

    @http.route('/payment/bitpay/ipn', type='json', auth='none')
    def bitpay_ipn(self, **post):
        """ Bitpay IPN. """
        cr, uid, context, env = request.cr, SUPERUSER_ID, request.context, request.env
        
        #_logger.info('REQUEST JSONREQUEST %s',pprint.pformat(request.jsonrequest))
        data = dict(request.jsonrequest)['data']
        invoiceId = data['id']
        
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'bitpay')])
        merchant_facade.fetch_token(self, acquirer.token)
        token = merchant_facade.client.tokens[acquirer.token]
        self.invoice = merchant_facade.get_from_bitpay_api(merchant_facade.client, merchant_facade.client.uri + "/invoices/" + invoiceId,token)
        #_logger.info('SELF INVOICE %s',pprint.pformat(self.invoice))

        tx = None
        if self.invoice['orderId']:
            tx_ids = request.registry['payment.transaction'].search(cr, uid, [('reference', '=', self.invoice['orderId'])], context=context)
            if tx_ids:
                tx = request.registry['payment.transaction'].browse(cr, uid, tx_ids[0], context=context)
                tx.bitpay_status = self.invoice['status']
        
        if self.invoice['status'] in ['confirmed']:
            tx.state = 'done'
            tx.sale_order_id.state = 'sale'
            if not tx.bitpay_buyerMailNotification and acquirer.buyerNotification:
                tx.sale_order_id.force_quotation_send()
                tx.bitpay_buyerMailNotification = "Send"
            tx.sale_order_id.order_line._action_procurement_create()
        elif self.invoice['status'] in ['paid']:
            tx.state = 'pending'
            tx.acquirer_id = acquirer.id
            tx.bitpay_txid =((self.invoice['transactions'])[0])['txid']
            tx.bitpay_invoiceId = invoiceId
        return ''

    @http.route(['/bitpay/checkout'], type='http', auth='none', csrf=None, website=True)
    def checkout(self, **post):
        #_logger.info('Bitpay datas %s', pprint.pformat(post))  # debug
        cr, uid, context, env = request.cr, SUPERUSER_ID, request.context, request.env
        acquirer = env['payment.acquirer'].sudo().browse(eval(post.get('acquirer')))
        currency = env['res.currency'].sudo().browse(eval(post.get('currency_id'))).name
        #_logger.info("Currency %s amount %s acquirer %s", currency, post.get('amount'), acquirer)      

        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        return_url = base_url + self._notify_url
       
        resp = merchant_facade.fetch_token(self, acquirer.token)
        token = merchant_facade.client.tokens[acquirer.token]
        if resp == '':
            acquirer.invoice = merchant_facade.client.create_invoice(
                {"price": post.get('amount'),
                "currency": currency,
                "orderId": post.get('reference'),
                "token": token,
                "redirectURL": acquirer.confirmationURL,
                "notificationURL": return_url,
                "notificationEmail": acquirer.notificationEmail,
                "extendedNotifications": True,
                "buyer": {  "email": post.get('partner_email'),
                            "name": post.get('partner_name'),
                            "address1": post.get('street1'),
                            "address2": post.get('street2'),
                            "locality": post.get('billing_partner_city'),
                            "postalCode": post.get('billing_partner_zip'),
                            "country": post.get('billing_partner_country_id'),
                            "notify": False}})
            invoiceId = dict(acquirer.invoice)['id']
            self.invoice = merchant_facade.get_from_bitpay_api(merchant_facade.client, merchant_facade.client.uri + "/invoices/" + invoiceId,token)

            #_logger.info("SELF INVOICE %s", pprint.pformat(self.invoice))
            return werkzeug.utils.redirect(self.invoice['url'])
        else:
            return werkzeug.utils.redirect(resp)