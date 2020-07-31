# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Survey Oniad",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "ont_base_survey",  # https://github.com/OdooNodrizaTech/ont
        "oniad_root",
        "crm",
        "crm_oniad",
        "survey"
    ],
    "data": [
        "views/survey_user_input_view.xml",
        "views/survey_survey_view.xml",
    ],        
    "installable": True
}

