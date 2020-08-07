# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_survey_id(self):
        super(CrmLead, self).get_survey_id()
        survey_id = 0
        if self.lead_oniad_type:
            survey_ids = self.env['survey.survey'].search(
                [
                    ('survey_lead_oniad_type', '=', self.lead_oniad_type),
                    ('survey_type', '=', 'popup'),
                    ('survey_subtype', '=', 'why_not'),
                    ('active', '=', True)
                ]
            )
            if survey_ids:
                survey_id = survey_ids[0].id

        return survey_id
