# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sendinblue_contact_id = fields.Many2one(
        comodel_name='sendinblue.contact',
        string='Sendinblue Contact'
    )
    sendinblue_list_id = fields.Many2one(
        comodel_name='sendinblue.list',
        string='Sendinblue List'
    )

    @api.multi
    def action_leads_create_sendinblue_list_id(self):
        self.ensure_one()
        return True
