# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveymonkeySurveyPage(models.Model):
    _name = 'surveymonkey.survey.page'
    _description = 'Surveymonkey Survey Page'
    
    survey_id = fields.Char(        
        string='Survey Id'
    )
    page_id = fields.Char(        
        string='Page Id'
    )        
    title = fields.Char(        
        string='Title'
    )
    description = fields.Text(        
        string='Description'
    )
    position = fields.Integer(        
        string='Position'
    )
    survey_survey_id = fields.Many2one(
        comodel_name='survey.survey',        
        string='Survey Id'
    )
    survey_page_id = fields.Many2one(
        comodel_name='survey.page',        
        string='Survey Id'
    )
        
    @api.multi    
    def cron_oniad_surveymonkey_generate_odoo_surveis(self, cr=None, uid=False, context=None):
        #surveymonkye.survey.page
        surveymonkey_survey_page_ids = self.env['surveymonkey.survey.page'].search([('survey_survey_id', '=', False),('survey_page_id', '=', False)])
        if len(surveymonkey_survey_page_ids)>0:
            for surveymonkey_survey_page_id in surveymonkey_survey_page_ids:
                #survey_survey
                if surveymonkey_survey_page_id.survey_survey_id.id==0:
                    surveymonkey_survey_page_ids2 = self.env['surveymonkey.survey.page'].search(
                        [
                            ('survey_survey_id', '!=', False),
                            ('survey_id', '=', surveymonkey_survey_page_id.survey_id)
                        ]
                    )
                    if len(surveymonkey_survey_page_ids2)==0:                                        
                        survey_survey_vals = {
                            'active': True,
                            'is_closed': False,
                            'title': surveymonkey_survey_page_id.title,
                            'users_can_go_back': False                                                                                                                                                                    
                        }                                                                                                
                        survey_survey_obj = self.env['survey.survey'].sudo().create(survey_survey_vals)
                        surveymonkey_survey_page_id.survey_survey_id = survey_survey_obj.id
                    else:
                        surveymonkey_survey_page_id.survey_survey_id = surveymonkey_survey_page_ids2[0].survey_survey_id.id
                #survey_page
                if surveymonkey_survey_page_id.survey_page_id.id==0:
                    survey_page_ids = self.env['survey.page'].search([('survey_id', '=', surveymonkey_survey_page_id.survey_survey_id.id)])
                                    
                    survey_page_vals = {
                        'title': surveymonkey_survey_page_id.title,
                        'survey_id': surveymonkey_survey_page_id.survey_survey_id.id,
                        'sequence': len(survey_page_ids)                                                                                                                                                                    
                    }                                                                                                
                    survey_page_obj = self.env['survey.page'].sudo().create(survey_page_vals)
                    surveymonkey_survey_page_id.survey_page_id = survey_page_obj.id
        #surveymonkey.survey.response
        surveymonkey_survey_response_ids = self.env['surveymonkey.survey.response'].search(
            [
                ('survey_user_input_id', '=', False),
                ('status', '=', 'completed')
            ]
        )        
        if len(surveymonkey_survey_response_ids)>0:
            for surveymonkey_survey_response_id in surveymonkey_survey_response_ids:
                surveymonkey_survey_page_ids = self.env['surveymonkey.survey.page'].search([('survey_id', '=', surveymonkey_survey_response_id.survey_id)])
                if len(surveymonkey_survey_page_ids)>0:
                    surveymonkey_survey_page_id = surveymonkey_survey_page_ids[0]
                        
                    survey_user_input_vals = {
                        'date_create': surveymonkey_survey_response_id.date_modified,
                        'email': surveymonkey_survey_response_id.ip_address,
                        'state': 'done',
                        'survey_id': surveymonkey_survey_page_id.survey_survey_id.id,
                        'type': 'manually',                                                                                                                                                                    
                    }                                                                                                
                    survey_user_input_obj = self.env['survey.user_input'].sudo().create(survey_user_input_vals)
                    surveymonkey_survey_response_id.survey_user_input_id = survey_user_input_obj.id        
        #surveymonkey.survey.response.custom.variable
        surveymonkey_survey_response_custom_variable_ids = self.env['surveymonkey.survey.response.custom.variable'].search([('survey_user_input_line_id', '=', False)])
        if len(surveymonkey_survey_response_custom_variable_ids)>0:
            for surveymonkey_survey_response_custom_variable_ids in surveymonkey_survey_response_custom_variable_ids:
                user_input_id = surveymonkey_survey_response_custom_variable_ids.surveymonkey_survey_response_id.survey_user_input_id.id
                page_id = surveymonkey_survey_response_custom_variable_ids.surveymonkey_survey_response_id.survey_user_input_id.survey_id.page_ids[0].id
                survey_id = surveymonkey_survey_response_custom_variable_ids.surveymonkey_survey_response_id.survey_user_input_id.survey_id.id                
                
                survey_question_ids = self.env['survey.question'].search(
                    [
                        ('survey_id', '=', survey_id),
                        ('question', '=', str(surveymonkey_survey_response_custom_variable_ids.field))
                    ]
                )
                if len(survey_question_ids)==0:                                        
                    survey_question_ids2 = self.env['survey.question'].search([('page_id', '=', page_id)])
                    
                    survey_question_vals = {
                        'page_id': page_id,
                        'question': str(surveymonkey_survey_response_custom_variable_ids.field),
                        'type': 'free_text',
                        'sequence': len(survey_question_ids2)                                                                                                                                                                    
                    }
                    survey_question_obj = self.env['survey.question'].sudo().create(survey_question_vals)
                else:
                    survey_user_input_line_vals = {
                        'page_id': page_id,
                        'question_id': survey_question_ids[0].id,
                        'survey_id': survey_id,
                        'user_input_id': user_input_id,
                        'value_free_text': surveymonkey_survey_response_custom_variable_ids.value,
                        'answer_type': 'free_text'
                    }
                    survey_user_input_line_obj = self.env['survey.user_input_line'].sudo().create(survey_user_input_line_vals)
                    surveymonkey_survey_response_custom_variable_ids.survey_user_input_line_id = survey_user_input_line_obj.id
        #surveymonkey.survey.response.question.answer
        surveymonkey_survey_response_question_answer_ids = self.env['surveymonkey.survey.response.question.answer'].search([('survey_user_input_line_id', '=', False)])
        if len(surveymonkey_survey_response_question_answer_ids)>0:
            for surveymonkey_survey_response_question_answer_id in surveymonkey_survey_response_question_answer_ids:
                page_id = surveymonkey_survey_response_question_answer_id.surveymonkey_survey_page_id.survey_page_id.id
                survey_id = surveymonkey_survey_response_question_answer_id.surveymonkey_survey_response_id.survey_user_input_id.survey_id.id
                user_input_id = surveymonkey_survey_response_question_answer_id.surveymonkey_survey_response_id.survey_user_input_id.id
                
                if surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.survey_question_id.id==0:
                    question_type = None
                    if surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.family=='open_ended' and surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.subtype=='essay':
                        question_type = 'free_text'
                    elif surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.family=='matrix' and surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.subtype=='rating':    
                        question_type = 'matrix'
                    elif surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.family=='single_choice':
                        question_type = 'simple_choice'
                    
                    if question_type!=None:                        
                        survey_question_vals = {
                            'page_id': page_id,
                            'question': str(surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.heading.encode('utf-8')),
                            'type': question_type,
                            'sequence': surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.position                                                                                                                                                                    
                        }
                        survey_question_obj = self.env['survey.question'].sudo().create(survey_question_vals)
                        surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.survey_question_id = survey_question_obj.id
                        #labels
                        if question_type=='matrix':
                            #label_ids (choice)
                            surveymonkey_question_choice_ids = self.env['surveymonkey.question.choice'].search([('surveymonkey_question_id', '=', surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.id)])
                            if len(surveymonkey_question_choice_ids)>0:
                                for surveymonkey_question_choice_id in surveymonkey_question_choice_ids:
                                    survey_label_vals = {
                                        'value': surveymonkey_question_choice_id.text,
                                        'question_id': surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.survey_question_id.id,
                                        'sequence': surveymonkey_question_choice_id.position                                                                                                                                                                    
                                    }
                                    survey_label_obj = self.env['survey.label'].sudo().create(survey_label_vals)
                                    surveymonkey_question_choice_id.survey_label_id = survey_label_obj.id                                                        
                            #label_ids_2 (row)
                            surveymonkey_question_row_ids = self.env['surveymonkey.question.row'].search([('surveymonkey_question_id', '=', surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.id)])
                            if len(surveymonkey_question_row_ids)>0:
                                for surveymonkey_question_row_id in surveymonkey_question_row_ids:
                                    survey_label_vals = {
                                        'value': surveymonkey_question_row_id.text,
                                        'question_id_2': surveymonkey_question_row_id.surveymonkey_question_id.survey_question_id.id,
                                        'sequence': surveymonkey_question_row_id.position                                                                                                                                                                    
                                    }
                                    survey_label_obj = self.env['survey.label'].sudo().create(survey_label_vals)
                                    surveymonkey_question_row_id.survey_label_id = survey_label_obj.id
                        elif question_type=='simple_choice':
                            #label_ids (choice)
                            surveymonkey_question_choice_ids = self.env['surveymonkey.question.choice'].search([('surveymonkey_question_id', '=', surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.id)])
                            if len(surveymonkey_question_choice_ids)>0:
                                for surveymonkey_question_choice_id in surveymonkey_question_choice_ids:
                                    survey_label_vals = {
                                        'value': surveymonkey_question_choice_id.text,
                                        'question_id': surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.survey_question_id.id,
                                        'sequence': surveymonkey_question_choice_id.position                                                                                                                                                                    
                                    }
                                    survey_label_obj = self.env['survey.label'].sudo().create(survey_label_vals)
                                    surveymonkey_question_choice_id.survey_label_id = survey_label_obj.id
                else:
                    question_type = str(surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.survey_question_id.type)
                
                    survey_user_input_line_vals = {
                        'page_id': page_id,
                        'question_id': surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.survey_question_id.id,
                        'survey_id': survey_id,
                        'user_input_id': user_input_id,
                        'answer_type': 'suggestion'
                    }
                    
                    if question_type=='free_text':
                        survey_user_input_line_vals['value_free_text'] = str(surveymonkey_survey_response_question_answer_id.text.encode('utf-8'))
                        survey_user_input_line_vals['answer_type'] = question_type
                    elif question_type=='simple_choice':
                        survey_user_input_line_vals['value_suggested'] = surveymonkey_survey_response_question_answer_id.surveymonkey_question_choice_id.survey_label_id.id
                    elif question_type=='matrix':
                        survey_user_input_line_vals['value_suggested'] = surveymonkey_survey_response_question_answer_id.surveymonkey_question_choice_id.survey_label_id.id
                        survey_user_input_line_vals['value_suggested_row'] = surveymonkey_survey_response_question_answer_id.surveymonkey_question_row_id.survey_label_id.id
                    
                    survey_user_input_line_obj = self.env['survey.user_input_line'].sudo().create(survey_user_input_line_vals)
                    surveymonkey_survey_response_question_answer_id.survey_user_input_line_id = survey_user_input_line_obj.id
        #define partner_id
        survey_user_input_ids = self.env['survey.user_input'].search([('partner_id', '=', False)])
        if len(survey_user_input_ids)>0:
            for survey_user_input_id in survey_user_input_ids:
                survey_question_ids = self.env['survey.question'].search(
                    [
                        ('survey_id', '=', survey_user_input_id.survey_id.id),
                        ('question', '=', 'partner_id'),
                    ]
                )
                if len(survey_question_ids)>0:
                    survey_question_id = survey_question_ids[0]
                    #get partner_id
                    survey_user_input_line_ids = self.env['survey.user_input_line'].search(
                        [
                            ('user_input_id', '=', survey_user_input_id.id),
                            ('question_id', '=', survey_question_id.id)
                        ]
                    )
                    if len(survey_user_input_line_ids)>0:
                        survey_user_input_line_id = survey_user_input_line_ids[0]
                        partner_id = int(survey_user_input_line_id)
                        res_partner_ids = self.env['res.partner'].search([('id', '=', partner_id)])
                        if len(res_partner_ids)>0:                        
                            survey_user_input_id.partner_id = partner_id
                else:
                    survey_question_ids = self.env['survey.question'].search(
                        [
                            ('survey_id', '=', survey_user_input_id.survey_id.id),
                            ('question', '=', 'oniad_user_id'),
                        ]
                    )
                    if len(survey_question_ids)>0:
                        survey_question_id = survey_question_ids[0]
                        #get oniad_user_id
                        survey_user_input_line_ids = self.env['survey.user_input_line'].search(
                            [
                                ('user_input_id', '=', survey_user_input_id.id),
                                ('question_id', '=', survey_question_id.id)
                            ]
                        )
                        if len(survey_user_input_line_ids)>0:
                            survey_user_input_line_id = survey_user_input_line_ids[0]
                            oniad_user_id = int(survey_user_input_line_id)
                            res_partner_ids = self.env['res.partner'].search([('oniad_user_id', '=', oniad_user_id)])
                            if len(res_partner_ids)>0:                        
                                survey_user_input_id.partner_id = res_partner_ids[0].id                                                                                                                                                                                                                                                                                                                       