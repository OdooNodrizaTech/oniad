# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, _
from datetime import datetime


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def action_leads_create_sendinblue_list_id(self):
        self.ensure_one()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        slack_log_channel = self.env['ir.config_parameter'].sudo().get_param(
            'slack_log_channel'
        )
        item_url = "%s/web?#id=%s&view_type=form&model=crm.lead" % (
            web_base_url,
            self.id
        )
        if self.type == 'lead':
            attachments = [
                {
                    "title": _('Lead create from Sendinblue *%s*') % self.name,
                    "color": "#36a64f",
                    "fallback": _("Ver iniciativa %s") % item_url,
                    "actions": [
                        {
                            "type": "button",
                            "text": _("Ver iniciativa"),
                            "url": item_url
                        }
                    ]
                }
            ]
        else:
            attachments = [
                {
                    "title": _('Lead create from Sendinblue *%s*') % self.name,
                    "color": "#36a64f",
                    "fallback": _("Ver flujo de ventas %s") % item_url,
                    "actions": [
                        {
                            "type": "button",
                            "text": _("Ver flujo de ventas"),
                            "url": item_url
                        }
                    ]
                }
            ]
        vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': slack_log_channel
        }
        self.env['slack.message'].sudo().create(vals)

    @api.model
    def cron_action_leads_date_deadline_today(self):
        current_date = datetime.today()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        lead_ids = self.env['crm.lead'].search(
            [
                ('active', '=', True),
                ('type', '=', 'opportunity'),
                ('user_id', '!=', False),
                ('date_deadline', '=', current_date.strftime("%Y-%m-%d"))
            ]
        )
        if lead_ids:
            for lead_id in lead_ids:
                if lead_id:
                    item_url = "%s/web?#id=%s&view_type=form&model=crm.lead" % (
                        web_base_url,
                        lead_id.id
                    )
                    if lead_id.user_id.slack_member_id:
                        attachments = [
                            {
                                "title": _('Today close planned lead *%s*') % (
                                    lead_id.name
                                ),
                                "color": "#36a64f",
                                "fallback": _("Ver flujo de ventas %s") % item_url,
                                "actions": [
                                    {
                                        "type": "button",
                                        "text": _("Ver flujo de ventas"),
                                        "url": item_url
                                    }
                                ]
                            }
                        ]
                        vals = {
                            'attachments': attachments,
                            'model': self._inherit,
                            'res_id': lead_id.id,
                            'as_user': True,
                            'channel': lead_id.user_id.slack_member_id
                        }
                        self.env['slack.message'].sudo().create(vals)
