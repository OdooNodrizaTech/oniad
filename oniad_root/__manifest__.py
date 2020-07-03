# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Oniad Root',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'base_vat', 'custom_day_due', 'crm', 'sale', 'survey', 'account', 'partner_financial_risk', 'website_portal_sale'],
    'data': [
        'data/ir_cron.xml',
        'data/ir_configparameter_data.xml',
        'views/account_invoice.xml',
        'views/account_payment.xml',
        'views/crm_lead.xml',
        'views/oniad_root_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/survey_user_input.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}