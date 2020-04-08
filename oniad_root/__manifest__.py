# -*- coding: utf-8 -*-
{
    'name': 'Oniad Root',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm', 'sale', 'survey', 'account', 'partner_financial_risk'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',
        'views/account_invoice.xml',
        'views/account_payment.xml',
        'views/crm_lead.xml',
        'views/oniad_root_view.xml',
        'views/res_partner_view.xml',
        'views/survey_user_input.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}