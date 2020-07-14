# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Partner financial risk Oniad',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'partner_financial_risk', 'account', 'oniad_root'],
    'data': [
        'data/ir_cron.xml',        
    ],
    'installable': True,
    'auto_install': False,    
}