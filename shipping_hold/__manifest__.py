# -*- coding: utf-8 -*-

{
    'name': 'Shipping Hold',
    'version': '15.0.1.0.0',
    'summary': 'Shipping Hold',
    'description': "",
    'license': 'LGPL-3',
    'website': 'https://www.aktivsoftware.com/',
    'depends': ['sale_management', 'stock'],
    'category': 'Management',
    'data': [
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "LGPL-3",
}
