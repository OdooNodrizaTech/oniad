# -*- coding: utf-8 -*-
{
    'name': 'Account OniAd',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'data/ir_cron.xml',        
        'views/account_invoice.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
        'views/account_payment.xml',
    ],
    'installable': True,
    'auto_install': False,    
}