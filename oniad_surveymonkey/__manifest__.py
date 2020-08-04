# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Oniad Surveymonkey",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "survey"
    ],
    "external_dependencies": {
        "python": [
            "pysftp"
        ],
    },
    "data": [
        "data/ir_configparameter_data.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
