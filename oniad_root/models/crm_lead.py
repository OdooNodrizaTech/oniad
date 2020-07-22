# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    oniad_campaign_id = fields.Many2one(
        comodel_name='oniad.campaign',
        string='Oniad Campaign'
    )
    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User'
    )
    oniad_user_id_link = fields.Char(
        compute='_oniad_user_id_link',
        string='OniAd User',
        store=False
    )

    @api.model
    def create(self, values):
        return_object = super(CrmLead, self).create(values)
        # oniad_user_id
        if return_object.partner_id:
            if return_object.partner_id.oniad_user_id:
                return_object.oniad_user_id = return_object.partner_id.oniad_user_id.id
        # return
        return return_object

    @api.multi
    def _oniad_user_id_link(self):
        for item in self:
            if item.oniad_user_id:
                item.oniad_user_id_link = 'https://platform.oniad.com/backend/admin/supadmin/card/%s' % item.oniad_user_id.id

    @api.one
    def action_send_mail_with_template_id(self, template_id=False):
        if template_id:
            mail_template_item = self.env['mail.template'].search([('id', '=', template_id)])[0]
            vals = {
                'author_id': 1,
                'record_name': self.name,
            }
            # Fix user_id
            if self.user_id.id > 0:
                vals['author_id'] = self.user_id.partner_id.id

                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo(self.user_id.id).create(vals)
            else:
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(vals)

            res = mail_compose_message_obj.onchange_template_id(
                mail_template_item.id,
                'comment',
                'crm.lead',
                self.id
            )

            mail_compose_message_obj.update({
                'author_id': vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'crm.lead',
                'res_id': self.id,
                'body': res['value']['body'],
                'subject': res['value']['subject'],
                'email_from': res['value']['email_from'],
                'partner_ids': res['value']['partner_ids'],
                # 'attachment_ids': res['value']['attachment_ids'],
                'record_name': res['record_name'],
                'no_auto_thread': False,
            })
            mail_compose_message_obj.send_mail_action()
            return True