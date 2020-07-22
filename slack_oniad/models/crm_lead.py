# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, tools
from datetime import datetime


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.one
    def action_leads_create_sendinblue_list_id(self, cr=None, uid=False, context=None):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        slack_log_channel = self.env['ir.config_parameter'].sudo().get_param('slack_log_channel')
        
        if self.type == 'lead':
            attachments = [
                {
                    "title": 'Se ha creado la iniciativa *%s* desde Sendinblue' % sefl.name,
                    "color": "#36a64f",
                    "fallback": "Ver iniciativa %s/web?#id=%s&view_type=form&model=crm.lead" % (web_base_url, self.id),
                    "actions": [
                        {
                            "type": "button",
                            "text": "Ver iniciativa",
                            "url": "%s/web?#id=%s&view_type=form&model=crm.lead" % (web_base_url, self.id)
                        }
                    ]                    
                }
            ]
        else:
            attachments = [
                {
                    "title": 'Se ha creado la oportunidad *%s* desde Sendinblue' % sefl.name,
                    "color": "#36a64f",
                    "fallback": "Ver flujo de ventas %s/web?#id=%s&view_type=form&model=crm.lead" % (web_base_url, self.id),
                    "actions": [
                        {
                            "type": "button",
                            "text": "Ver flujo de ventas",
                            "url": "%s/web?#id=%s&view_type=form&model=crm.lead" % (web_base_url, self.id)
                        }
                    ]                    
                }
            ]                                   
        
        vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': slack_log_channel,                                                         
        }                        
        self.env['slack.message'].sudo().create(vals)
    
    @api.multi
    def cron_action_leads_date_deadline_today(self, cr=None, uid=False, context=None):
        current_date = datetime.today()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        crm_lead_ids = self.env['crm.lead'].search(
            [
                ('active', '=', True),
                ('type', '=', 'opportunity'),
                ('user_id', '!=', False),
                ('date_deadline', '=', current_date.strftime("%Y-%m-%d"))
            ]
        )        
        if crm_lead_ids:
            for crm_lead_id in crm_lead_ids:
                if crm_lead_id:
                    if crm_lead_id.user_id.slack_member_id:
                        attachments = [
                            {
                                "title": 'Te recordamos que hoy es el cierre previsto del flujo  *%s*' % crm_lead_id.name,
                                "color": "#36a64f",
                                "fallback": "Ver flujo de ventas %s/web?#id=%s&view_type=form&model=crm.lead" % (web_base_url, crm_lead_id.id),
                                "actions": [
                                    {
                                        "type": "button",
                                        "text": "Ver flujo de ventas",
                                        "url": "%s/web?#id=%s&view_type=form&model=crm.lead" % (web_base_url, crm_lead_id.id)
                                    }
                                ]                    
                            }
                        ]
                        vals = {
                            'attachments': attachments,
                            'model': self._inherit,
                            'res_id': crm_lead_id.id,
                            'as_user': True,
                            'channel': crm_lead_id.user_id.slack_member_id,                                                         
                        }                        
                        self.env['slack.message'].sudo().create(vals)