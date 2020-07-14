# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.one
    def action_leads_create_sendinblue_list_id(self, cr=None, uid=False, context=None):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        slack_log_channel = self.env['ir.config_parameter'].sudo().get_param('slack_log_channel')
        
        if self.type=='lead':
            attachments = [
                {                    
                    "title": 'Se ha creado la iniciativa *'+str(self.name)+'* desde Sendinblue',                        
                    "color": "#36a64f",                                            
                    "fallback": "Ver iniciativa "+str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=crm.lead",
                    "actions": [
                        {
                            "type": "button",
                            "text": "Ver iniciativa",
                            "url": str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=crm.lead"
                        }
                    ]                    
                }
            ]
        else:
            attachments = [
                {                    
                    "title": 'Se ha creado la oportunidad *'+str(self.name)+'* desde Sendinblue',                        
                    "color": "#36a64f",                                            
                    "fallback": "Ver flujo de ventas "+str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=crm.lead",
                    "actions": [
                        {
                            "type": "button",
                            "text": "Ver flujo de ventas",
                            "url": str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=crm.lead"
                        }
                    ]                    
                }
            ]                                   
        
        slack_message_vals = {                        
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': slack_log_channel,                                                         
        }                        
        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)
    
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
        if crm_lead_ids!=False:
            for crm_lead_id in crm_lead_ids:
                if crm_lead_id.id>0:
                    if crm_lead_id.user_id.slack_member_id!=False:
                        attachments = [
                            {                    
                                "title": 'Te recordamos que hoy es el cierre previsto del flujo  *'+str(crm_lead_id.name)+'*',                        
                                "color": "#36a64f",                                            
                                "fallback": "Ver flujo de ventas "+str(web_base_url)+"/web?#id="+str(crm_lead_id.id)+"&view_type=form&model=crm.lead",
                                "actions": [
                                    {
                                        "type": "button",
                                        "text": "Ver flujo de ventas",
                                        "url": str(web_base_url)+"/web?#id="+str(crm_lead_id.id)+"&view_type=form&model=crm.lead"
                                    }
                                ]                    
                            }
                        ]                        
                        
                        slack_message_vals = {                        
                            'attachments': attachments,
                            'model': self._inherit,
                            'res_id': crm_lead_id.id,
                            'as_user': True,
                            'channel': crm_lead_id.user_id.slack_member_id,                                                         
                        }                        
                        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)