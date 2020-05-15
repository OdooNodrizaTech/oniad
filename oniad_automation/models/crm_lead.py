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

    @api.model    
    def cron_automation_welcome_leads(self):        
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        #skip_cron
        skip_cron = True
        
        weekday = current_date.weekday()
        current_date_hour = current_date.strftime("%H")    
                        
        hours_allow_by_weekday = {
            '0': ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],#Lunes
            '1': ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],#Martes
            '2': ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],#Miercoles
            '3': ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],#Jueves
            '4': ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],#Viernes
        }

        if str(weekday) in hours_allow_by_weekday:
            hours_allow = hours_allow_by_weekday[str(weekday)]        
            if current_date_hour in hours_allow:            
                skip_cron = False                      
        
        if skip_cron==False:
            oniad_automation_welcome_lead_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('oniad_automation_welcome_lead_mail_template_id'))
            #automation_log
            automation_log_ids = self.env['automation.log'].search([('model', '=', 'crm.lead'),('category', '=', 'crm_lead'),('action', '=', 'send_mail_welcome')])
            crm_lead_ids_get_not_in = automation_log_ids.mapped('res_id')            
            #mail_message_subtype                 
            mail_message_subtype_ids = self.env['mail.message.subtype'].search([('res_model', '=', 'crm.lead'),('id', 'not in', [7,8,9,10])])
            mail_message_subtype_ids_in = mail_message_subtype_ids.mapped('id')
            mail_message_subtype_ids_in.append(1)#Add Debates-General
            #date_action 
            date_action = datetime(current_date.year, current_date.month, current_date.day) + relativedelta(days=7)            
            #crm_leads
            crm_lead_ids = self.env['crm.lead'].search(
                [
                    ('type', '=', 'opportunity'),
                    ('active', '=', True),
                    ('probability', '>', 0),
                    ('probability', '<', 100),
                    ('user_id', '!=', False),                    
                    ('commercial_activity_type', '=', 'account'),
                    ('lead_oniad_type', '=', 'welcome'),
                    ('partner_id.phone', '=', False),
                    ('partner_id.mobile', '=', False),
                    ('id', 'not in', crm_lead_ids_get_not_in)
                ]
            )
            if len(crm_lead_ids)>0:
                for crm_lead_id in crm_lead_ids:
                    crm_activity_report_ids = self.env['crm.activity.report'].search(
                        [
                            ('active', '=', True),
                            ('lead_id', '=', crm_lead_id.id),
                            ('subtype_id', 'in', mail_message_subtype_ids_in)                             
                        ]
                    )
                    if len(crm_activity_report_ids)==0:
                        #action_send_mail_with_template_id
                        crm_lead_id.action_send_mail_with_template_id(oniad_automation_welcome_lead_mail_template_id)
                        #save_log
                        automation_log_vals = {                    
                            'model': 'crm.lead',
                            'res_id': crm_lead_id.id,
                            'category': 'crm_lead',
                            'action': 'send_mail_welcome',                                                                                                                                                                                           
                        }
                        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                        #update
                        crm_lead_id.write({
                            'next_activity_id': 3,#Tarea
                            'date_action': date_action.strftime("%Y-%m-%d"),
                            'title_action': 'Revisar contacto usuario'
                        })
                        #save_log
                        automation_log_vals = {                    
                            'model': 'crm.lead',
                            'res_id': crm_lead_id.id,
                            'category': 'crm_lead',
                            'action': 'assign_next_activity_id_3',                                                                                                                                                                                           
                        }
                        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                        #stage_id
                        if crm_lead_id.stage_id.id!=2:
                            crm_lead_id.write({
                                'stage_id': 2,#Ayuda ofrecida
                            })
                            #save_log
                            automation_log_vals = {                    
                                'model': 'crm.lead',
                                'res_id': crm_lead_id.id,
                                'category': 'crm_lead',
                                'action': 'change_stage_id_2',                                                                                                                                                                                           
                            }
                            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)