# -*- coding: utf-8 -*-
{
    'name': 'Oniad Automation',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'automation_log'],
    'data': [
        'data/ir_configparameter_data.xml',
        'data/ir_cron.xml',                 
    ],    
    'installable': True,
    'auto_install': False,    
}