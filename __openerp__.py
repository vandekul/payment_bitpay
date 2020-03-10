{
    'name': "Bitcoin Payment Acquirer",
    'version': '9.0',
    'category' : 'Payment',
    'website': 'https://github.com/mumaker',
    'summary':  """Bitcoin Payment Gateway.""",
    'description': """Payment Acquirer: Bitcoin""",
    'author': 'mumaker',
    'depends': ['payment', 'base', 'website_sale'],
    'data': [
        'views/views.xml',
        'views/template.xml',
        'data/bitcoin.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True
}

{
    'name': "Gateway BitPay",

    'summary': """This module integrates BitPay - pay with Bitcoin, Litecoin, Ethereum, Ripple or similar Cryptocurrency - with Odoo v9.0""",
    'author': "Vandekul",
    'website': "https://github.com/vandekul",
    'category': 'Website',
    'version': '9.0c',
    'license': 'GPL-3',
    'application': True,
    'depends': ['base', 'payment'],
    'data': [
        'views/payment_bitpay_templates.xml',
        'views/bitpay_configuration_view.xml',
        'data/payment_acquirer_data.xml'
    ],
    'installable': True,
    'auto_install': False,
    'description': 'static/description/index.html',
    'images': ['static/description/icon.png', 'static/description/main_screenshot.png'],
}