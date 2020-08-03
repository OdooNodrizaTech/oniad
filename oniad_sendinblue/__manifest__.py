# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Oniad Sendinblue",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale"
    ],
    "data": [
        "views/sendinblue_view.xml",
        "views/crm_lead_view.xml",
        "data/ir_configparameter_data.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
    ],
    "external_dependencies": {
        "python": [
            "sib_api_v3_sdk"
        ],
    },
    "installable": True
}
