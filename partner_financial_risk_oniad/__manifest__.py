# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner financial risk Oniad",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "partner_financial_risk",  # https://github.com/OdooNodrizaTech/financial_risk
        "account",
        "oniad_root"
    ],
    "data": [
        "data/ir_cron.xml",
    ],
    "installable": True
}
