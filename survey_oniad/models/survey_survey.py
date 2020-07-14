# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

import uuid
import pytz

import logging
_logger = logging.getLogger(__name__)

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    
    survey_lead_oniad_type = fields.Selection(
        selection=[
            ('none','Ninguno'),
            ('welcome','Bienvenida'), 
            ('sleep','Dormido'), 
            ('catchment','Captacion'),
            ('other','Otro')                         
        ],
        default='none',
        string='Tipo de lead'
    )
    oniad_user_type = fields.Selection(
        [
            ('all', 'Todos'),
            ('no_agency', 'No agencias (usuarios y cuentas creadas)'),
            ('agency', 'Agencias'),
            ('user', 'Usuarios'),
            ('user_without_parent_id','Usuarios NO vinculados'),
            ('user_with_parent_id','Usuarios SI vinculados')                    
        ],
        size=15, 
        string='Oniad User type'
    )
    oniad_campaign_spent_limit_from = fields.Integer(
        string='Oniad Campaign Spent Limit From',
    )
    
    @api.one    
    def get_oniad_user_ids_first_spent(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        oniad_user_ids = False
        
        if self.automation_difference_days>0:
            #date_filters
            date_filter_start = current_date + relativedelta(days=-self.automation_difference_days*2)
            date_filter_end = current_date + relativedelta(days=-self.automation_difference_days)            
            #oniad_user_ids
            if self.oniad_user_type=='all':
                oniad_user_ids_filter = self.env['oniad.user'].search(
                    [ 
                        ('spent_cost', '>=', self.oniad_campaign_spent_limit_from),
                        ('partner_id', '!=', False),                
                        ('spent_min_date', '!=', False),                        
                        ('spent_min_date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('spent_min_date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )
            elif self.oniad_user_type in ['agency', 'user']:
                oniad_user_ids_filter = self.env['oniad.user'].search(
                    [ 
                        ('spent_cost', '>=', self.oniad_campaign_spent_limit_from),
                        ('type', '=', self.oniad_user_type),
                        ('partner_id', '!=', False),                
                        ('spent_min_date', '!=', False),
                        ('spent_min_date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('spent_min_date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )
            elif self.oniad_user_type=='user_without_parent_id':
                oniad_user_ids_filter = self.env['oniad.user'].search(
                    [ 
                        ('spent_cost', '>=', self.oniad_campaign_spent_limit_from),
                        ('type', '=', 'user'),
                        ('parent_id', '=', False),
                        ('partner_id', '!=', False),                
                        ('spent_min_date', '!=', False),
                        ('spent_min_date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('spent_min_date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )
            elif self.oniad_user_type=='user_with_parent_id':
                oniad_user_ids_filter = self.env['oniad.user'].search(
                    [ 
                        ('spent_cost', '>=', self.oniad_campaign_spent_limit_from),
                        ('type', '=', 'user'),
                        ('parent_id', '!=', False),
                        ('partner_id', '!=', False),                
                        ('spent_min_date', '!=', False),
                        ('spent_min_date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('spent_min_date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )                                
            else:
                oniad_user_ids_filter = self.env['oniad.user'].search(
                    [ 
                        ('spent_cost', '>=', self.oniad_campaign_spent_limit_from),                        
                        ('type', 'in', ('user', 'client_own')),
                        ('partner_id', '!=', False),                
                        ('spent_min_date', '!=', False),
                        ('spent_min_date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('spent_min_date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )                                
            #operations
            if len(oniad_user_ids_filter)>0:                                
                #survey_user_input_ids
                survey_user_input_ids = self.env['survey.user_input'].search(
                    [ 
                        ('survey_id.survey_type', '=', self.survey_type),
                        ('survey_id.survey_subtype', '=', self.survey_subtype),                                        
                        ('oniad_user_id', 'in', oniad_user_ids_filter.ids),                                        
                    ]
                )                
                if len(survey_user_input_ids)>0:                        
                    oniad_user_ids = self.env['oniad.user'].search(
                        [ 
                            ('id', 'in', oniad_user_ids_filter.ids),
                            ('id', 'not in', survey_user_input_ids.mapped('oniad_user_id').ids)                                                
                        ]
                    )
                else:
                    oniad_user_ids = self.env['oniad.user'].search([('id', 'in', oniad_user_ids_filter.ids)])                                
        #oniad_user_ids                
        return oniad_user_ids
    
    @api.one    
    def get_oniad_user_ids_recurrent(self):
        #general
        survey_frequence_days = {
            'day': 1,
            'week': 7,
            'month': 30,
            'year': 365
        }
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        oniad_user_ids = False
        
        if self.automation_difference_days>0:
            #date_filters
            date_filter_end = current_date
            date_filter_start = current_date + relativedelta(days=-self.automation_difference_days)                        
            #oniad_transaction_ids
            if self.oniad_user_type=='all':
                oniad_transaction_ids = self.env['oniad.transaction'].search(
                    [ 
                        ('oniad_user_id.partner_id', '!=', False),                                        
                        ('date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )
            elif self.oniad_user_type in ['agency', 'user']:
                oniad_transaction_ids = self.env['oniad.transaction'].search(
                    [ 
                        ('oniad_user_id.partner_id', '!=', False),
                        ('oniad_user_id.type', '=', self.oniad_user_type),                                        
                        ('date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )                
            elif self.oniad_user_type=='user_without_parent_id':
                oniad_transaction_ids = self.env['oniad.transaction'].search(
                    [ 
                        ('oniad_user_id.partner_id', '!=', False),
                        ('oniad_user_id.type', '=', 'user'),
                        ('oniad_user_id.parent_id', '=', False),                                        
                        ('date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )                
            elif self.oniad_user_type=='user_with_parent_id':
                oniad_transaction_ids = self.env['oniad.transaction'].search(
                    [ 
                        ('oniad_user_id.partner_id', '!=', False),
                        ('oniad_user_id.type', '=', 'user'),
                        ('oniad_user_id.parent_id', '!=', False),                                        
                        ('date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )                                                
            else:
                oniad_transaction_ids = self.env['oniad.transaction'].search(
                    [ 
                        ('oniad_user_id.partner_id', '!=', False),
                        ('oniad_user_id.type', 'in', ('user', 'client_own')),                                        
                        ('date', '>', date_filter_start.strftime("%Y-%m-%d")),
                        ('date', '<', date_filter_end.strftime("%Y-%m-%d")),                
                    ]
                )
            #operations
            if len(oniad_transaction_ids)>0:
                oniad_user_ids_all = {}
                
                for oniad_transaction_id in oniad_transaction_ids:
                    if oniad_transaction_id.oniad_user_id.id not in oniad_user_ids_all:
                        oniad_user_ids_all[oniad_transaction_id.oniad_user_id.id] = 0
                    #increase_amount
                    oniad_user_ids_all[oniad_transaction_id.oniad_user_id.id] += oniad_transaction_id.amount
                #filter amount
                oniad_user_ids_real = []                 
                for oniad_user_id_all in oniad_user_ids_all:
                    amount_item = oniad_user_ids_all[oniad_user_id_all]
                    
                    if amount_item>=self.oniad_campaign_spent_limit_from:
                        oniad_user_ids_real.append(oniad_user_id_all)
                #final
                if len(oniad_user_ids_real)>0:
                    #operations
                    oniad_user_ids_max_date_survey_user_input = {}
                    for oniad_user_id_real in oniad_user_ids_real:
                        if oniad_user_id_real not in oniad_user_ids_max_date_survey_user_input:
                            oniad_user_ids_max_date_survey_user_input[oniad_user_id_real] = None                                        
                    #survey_user_input_ids
                    survey_user_input_ids = self.env['survey.user_input'].search(
                        [ 
                            ('survey_id.survey_type', '=', self.survey_type),
                            ('survey_id.survey_subtype', '=', self.survey_subtype),                                        
                            ('oniad_user_id', 'in', oniad_user_ids_real)                                        
                        ]
                    )
                    if len(survey_user_input_ids)>0:
                        #operations
                        for survey_user_input_id in survey_user_input_ids:
                            date_create_item_format = datetime.strptime(survey_user_input_id.date_create, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
                            
                            if oniad_user_ids_max_date_survey_user_input[survey_user_input_id.oniad_user_id.id]==None:
                                oniad_user_ids_max_date_survey_user_input[survey_user_input_id.oniad_user_id.id] = date_create_item_format
                            else:
                                if date_create_item_format>oniad_user_ids_max_date_survey_user_input[survey_user_input_id.oniad_user_id.id]:
                                    oniad_user_ids_max_date_survey_user_input[survey_user_input_id.oniad_user_id.id] = date_create_item_format
                    #operations
                    oniad_user_ids_final = []                            
                    b = datetime.strptime(date_filter_end.strftime("%Y-%m-%d"), "%Y-%m-%d")
                    survey_frequence_days_item = survey_frequence_days[self.survey_frequence]
                    for oniad_user_id in oniad_user_ids_max_date_survey_user_input:
                        oniad_user_id_item = oniad_user_ids_max_date_survey_user_input[oniad_user_id]
                        #checks
                        if oniad_user_id_item==None:
                            oniad_user_ids_final.append(oniad_user_id)
                        else:
                            a = datetime.strptime(oniad_user_id_item, "%Y-%m-%d")                                
                            delta = b - a
                            difference_days = delta.days                                                                                                            
                            if difference_days>=survey_frequence_days_item:
                                oniad_user_ids_final.append(oniad_user_id)                                    
                    #final                                                                    
                    oniad_user_ids = self.env['oniad.user'].search([('id', 'in', oniad_user_ids_final)])                                           
        #return            
        return oniad_user_ids                            
    
    @api.one    
    def send_survey_satisfaction_phone(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid'))
        #deadline
        deadline = False                
        if self.deadline_days>0:
            deadline = current_date + relativedelta(days=self.deadline_days)                
        #ANADIMOS LOS QUE CORRESPONDEN (NUEVOS)
        oniad_user_ids = self.get_oniad_user_ids_first_spent()[0]#Fix multi
        if oniad_user_ids!=False:
            if len(oniad_user_ids)>0:                        
                for oniad_user_id in oniad_user_ids:
                    #token
                    token = uuid.uuid4().__str__()                                        
                    #creamos el registro personalizado SIN asignar a nadie
                    survey_user_input_vals = {
                        'oniad_user_id': oniad_user_id.id,
                        #'user_id': sale_order_id.user_id.id,#Fix prevent assign 'incorrectly'
                        'state': 'skip',
                        'type': 'manually',
                        'token': token,
                        'survey_id': self.id,
                        'partner_id': oniad_user_id.partner_id.id,
                        'test_entry': False
                    }
                    #deadline (if is need)
                    if deadline!=False:
                        survey_user_input_vals['deadline'] = deadline
                    #create
                    survey_user_input_obj = self.env['survey.user_input'].sudo().create(survey_user_input_vals)
        #return
        return False
        
    @api.one    
    def send_survey_satisfaction_recurrent_phone(self):
        current_date = datetime.now(pytz.timezone('Europe/Madrid')) 
        #deadline
        deadline = False                
        if self.deadline_days>0:
            deadline = current_date + relativedelta(days=self.deadline_days)                
        #ANADIMOS LOS QUE CORRESPONDEN (NUEVOS)
        oniad_user_ids = self.get_oniad_user_ids_recurrent()[0]#Fix multi
        if oniad_user_ids!=False:
            if len(oniad_user_ids)>0:                        
                #operations
                for oniad_user_id in oniad_user_ids:                
                    #token
                    token = uuid.uuid4().__str__()                                        
                    #creamos el registro personalizado SIN asignar a nadie
                    survey_user_input_vals = {
                        'oniad_user_id': oniad_user_id.id,                                    
                        #'user_id': sale_order_id.user_id.id,#Fix prevent assign 'incorrectly'
                        'state': 'skip',
                        'type': 'manually',
                        'token': token,
                        'survey_id': self.id,
                        'partner_id': oniad_user_id.partner_id.id,
                        'test_entry': False
                    }
                    #deadline (if is need)
                    if deadline!=False:
                        survey_user_input_vals['deadline'] = deadline
                    #create
                    survey_user_input_obj = self.env['survey.user_input'].sudo().create(survey_user_input_vals)
        #return
        return False        
    
    @api.one    
    def send_survey_real_satisfaction_mail(self):
        oniad_user_ids = self.get_oniad_user_ids_first_spent()[0]#Fix multi                                        
        #operations
        if len(oniad_user_ids)>0:
            for oniad_user_id in oniad_user_ids:
                self.send_survey_real_by_oniad_user_id(self, oniad_user_id.partner_id, oniad_user_id)
        #return
        return False
        
    @api.one    
    def send_survey_satisfaction_mail(self, survey_survey_input_expired_ids):
        if len(survey_survey_input_expired_ids)>0:
            #actual_results
            survey_survey_input_ids = self.env['survey.user_input'].search([('survey_id', '=', self.id)])
            #query
            if len(survey_survey_input_expired_ids)>0:
                oniad_user_ids = self.env['oniad.user'].search(
                    [ 
                        ('id', 'in', survey_survey_input_expired_ids.mapped('oniad_user_id').ids),
                        ('id', 'not in', survey_survey_input_ids.mapped('oniad_user_id').ids),                                                
                    ]
                )
            else:
                oniad_user_ids = self.env['oniad.user'].search([('id', 'in', survey_survey_input_expired_ids.mapped('oniad_user_id').ids)])
            #operations
            if len(oniad_user_ids)>0:
                for oniad_user_id in oniad_user_ids:                                
                    self.send_survey_real_by_oniad_user_id(self, oniad_user_id.partner_id, oniad_user_id)
        #return
        return False                                                        
    
    @api.one    
    def send_survey_real_satisfaction_recurrent_mail(self):
        oniad_user_ids = self.get_oniad_user_ids_recurrent()[0]#Fix multi                                        
        #operations
        if oniad_user_ids!=False:
            if len(oniad_user_ids)>0:
                for oniad_user_id in oniad_user_ids:
                    self.send_survey_real_by_oniad_user_id(self, oniad_user_id.partner_id, oniad_user_id)
        #return
        return False
    
    @api.one    
    def send_survey_satisfaction_recurrent_mail(self, survey_survey_input_expired_ids):
        if len(survey_survey_input_expired_ids)>0:
            #actual_results
            survey_survey_input_ids = self.env['survey.user_input'].search([('survey_id', '=', self.id)])
            #query
            if len(survey_survey_input_expired_ids)>0:
                oniad_user_ids = self.env['oniad.user'].search(
                    [ 
                        ('id', 'in', survey_survey_input_expired_ids.mapped('oniad_user_id').ids),
                        ('id', 'not in', survey_survey_input_ids.mapped('oniad_user_id').ids)                                                
                    ]
                )
            else:
                oniad_user_ids = self.env['oniad.user'].search([('id', 'in', survey_survey_input_expired_ids.mapped('oniad_user_id').ids)])
            #operations
            if len(oniad_user_ids)>0:
                for oniad_user_id in oniad_user_ids:                                
                    self.send_survey_real_by_oniad_user_id(self, oniad_user_id.partner_id, oniad_user_id)
        #return
        return False                    
    
    @api.multi    
    def send_survey_real_by_oniad_user_id(self, survey_survey, partner_id, oniad_user_id):
        #survey_mail_compose_message_vals                                                                                                                                                    
        survey_mail_compose_message_vals = {
            'auto_delete_message': False,
            'template_id': survey_survey.mail_template_id.id,
            'subject': survey_survey.mail_template_id.subject,
            'res_id': survey_survey.id,
            'body': survey_survey.mail_template_id.body_html,
            'record_name': survey_survey.title,
            'no_auto_thread': False,
            'public': 'email_private',
            'reply_to': survey_survey.mail_template_id.reply_to,
            'model': 'survey.survey',
            'survey_id': survey_survey.id,
            'message_type': 'comment',
            'email_from': survey_survey.mail_template_id.email_from,
            'partner_ids': []
        }
        #Fix
        partner_id_partial = (4, partner_id.id)
        survey_mail_compose_message_vals['partner_ids'].append(partner_id_partial)            
        #survey_mail_compose_message_obj                                                                                                    
        survey_mail_compose_message_obj = self.env['survey.mail.compose.message'].sudo().create(survey_mail_compose_message_vals)                
        survey_mail_compose_message_obj.oniad_send_partner_mails({
            partner_id.id: {'oniad_user_id': oniad_user_id}
        })
        
    @api.multi    
    def send_survey_real_by_oniad_campaign_id(self, survey_survey, partner_id, oniad_campaign_id):
        #survey_mail_compose_message_vals                                                                                                                                                    
        survey_mail_compose_message_vals = {
            'auto_delete_message': False,
            'template_id': survey_survey.mail_template_id.id,
            'subject': survey_survey.mail_template_id.subject,
            'res_id': survey_survey.id,
            'body': survey_survey.mail_template_id.body_html,
            'record_name': survey_survey.title,
            'no_auto_thread': False,
            'public': 'email_private',
            'reply_to': survey_survey.mail_template_id.reply_to,
            'model': 'survey.survey',
            'survey_id': survey_survey.id,
            'message_type': 'comment',
            'email_from': survey_survey.mail_template_id.email_from,
            'partner_ids': []
        }
        #Fix
        partner_id_partial = (4, partner_id.id)
        survey_mail_compose_message_vals['partner_ids'].append(partner_id_partial)            
        #survey_mail_compose_message_obj                                                                                                    
        survey_mail_compose_message_obj = self.env['survey.mail.compose.message'].sudo().create(survey_mail_compose_message_vals)                
        survey_mail_compose_message_obj.oniad_send_partner_mails({
            partner_id.id: {'oniad_campaign_id': oniad_campaign_id}
        })                    