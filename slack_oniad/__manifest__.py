# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Slack Oniad",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "crm",
        "account",
        "slack",  # https://github.com/OdooNodrizaTech/slack
        "oniad_root"
    ],
    "data": [
        "data/ir_cron.xml",
    ],    
    "installable": True
}
