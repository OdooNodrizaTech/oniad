# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account OniAd",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "partner_financial_risk_oniad"
    ],
    "external_dependencies": {
        "python": [
            "boto3"
        ],
    },
    "data": [
        "data/ir_cron.xml",
        "views/account_invoice_view.xml",
        "views/account_move_view.xml",
        "views/account_move_line_view.xml",
        "views/account_payment_view.xml",
    ],
    "installable": True
}
