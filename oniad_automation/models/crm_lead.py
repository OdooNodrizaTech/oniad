# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.one
    def action_send_mail_with_template_id(self, template_id=False):
        if template_id!=False:                                        
            mail_template_item = self.env['mail.template'].search([('id', '=', template_id)])[0]                                
            mail_compose_message_vals = {                    
                'author_id': self.user_id.partner_id.id,
                'record_name': self.name,                                                                                                                                                                                           
            }
            mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo(self.user_id.id).create(mail_compose_message_vals)
            return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_item.id, 'comment', 'crm.lead', self.id)                                
            
            mail_compose_message_obj.update({
                'author_id': mail_compose_message_vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'crm.lead',
                'res_id': self.id,
                'body': return_onchange_template_id['value']['body'],
                'subject': return_onchange_template_id['value']['subject'],
                'email_from': return_onchange_template_id['value']['email_from'],
                'partner_ids': return_onchange_template_id['value']['partner_ids'],
                #'attachment_ids': return_onchange_template_id['value']['attachment_ids'],
                'record_name': mail_compose_message_vals['record_name'],
                'no_auto_thread': False,                     
            })                                         
            mail_compose_message_obj.send_mail()                                                                                                                
            return True