# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Oniad Root",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail",
        "base_vat",
        "custom_day_due",  # https://github.com/OdooNodrizaTech/account
        "crm",
        "sale",
        "survey",
        "account",
        "account_payment_mode",  # https://github.com/OCA/bank-payment
        "account_payment_partner",  # https://github.com/OCA/bank-payment
        "account_payment_sale",  # https://github.com/OCA/bank-payment
        "partner_financial_risk",  # https://github.com/OdooNodrizaTech/financial_risk
        "website",
        "mail_activity_done"  # https://github.com/OCA/social
    ],
    "external_dependencies": {
        "python": [
            "boto3"
        ],
    },
    "data": [
        "data/ir_cron.xml",
        "data/ir_configparameter_data.xml",
        "views/account_invoice_view.xml",
        "views/account_payment_view.xml",
        "views/crm_lead_view.xml",
        "views/oniad_root_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "views/survey_user_input_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True
}
