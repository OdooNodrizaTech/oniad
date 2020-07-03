# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

import psycopg2

from ..surveymonkey.web_service import SurveymonkeyWebService

class SurveymonkeySurveyResponse(models.Model):
    _name = 'surveymonkey.survey.response'
    _description = 'Surveymonkey Survey Response'
    
    survey_id = fields.Char(        
        string='Survey Id'
    )
    response_id = fields.Char(        
        string='Response Id'
    )
    collector_id = fields.Char(        
        string='Collector Id'
    )
    total_time = fields.Integer(        
        string='Total time'
    )            
    status = fields.Char(        
        string='Estado'
    )
    ip_address = fields.Char(        
        string='IP'
    )
    date_modified = fields.Date(        
        string='Fecha modificado'
    )
    survey_user_input_id = fields.Many2one(
        comodel_name='survey.user_input',        
        string='Survey User Input Id'
    )    
    
    def connect_postgresql_datawarehouse_rds(self):
        try:
            connection = psycopg2.connect(
                user = str(self.env['ir.config_parameter'].sudo().get_param('survey_oniad_datawarehouse_rds_user')),
                password = str(self.env['ir.config_parameter'].sudo().get_param('survey_oniad_datawarehouse_rds_password')),
                host = str(self.env['ir.config_parameter'].sudo().get_param('survey_oniad_datawarehouse_rds_endpoint')),
                port = "5432",
                database = str(self.env['ir.config_parameter'].sudo().get_param('survey_oniad_datawarehouse_rds_database'))
            )            
            return {
                'connection': connection,
                'errors': False,
                'error': ''
            }            
        except (psycopg2.Error) as error :
            return {
                'connection': False,
                'errors': True,
                'error': error
            }
            
    @api.multi    
    def cron_surveymonkey_survey_response_items_send_datawarehouse(self, cr=None, uid=False, context=None):                
        #connect_postgresql_datawarehouse_rds
        return_connection = self.connect_postgresql_datawarehouse_rds()
        
        if return_connection['errors']==True:
            _logger.info(return_connection['error'])
        else:                                                           
            #question_codes        
            question_codes = {
                #Atención al cliente                    
                'ATC.01.GLO.General': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242441046,                            
                            'row_id': 0
                        },                        
                    }
                },
                'ATC.02.GLO.Amabilidad': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242437062,
                            'row_id': 1654070688
                        },                        
                    }
                },
                'ATC.03.GLO.Profesionalidad': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242437062,
                            'row_id': 1654070691
                        },                        
                    }
                },
                'ATC.04.GLO.Claridad': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242437062,                            
                            'row_id': 1654070693
                        },                        
                    }
                },
                'ATC.05.GLO.Necesidades': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242440655,
                            'row_id': 0,
                        },                        
                    }
                },                 
                #Producto
                'PRO.01.GLO.General': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242426124,
                            'row_id': 0
                        },                        
                    }
                },
                'PRO.02.GLO.Utilidad': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242426123,
                            'row_id': 0
                        },                        
                    }
                },
                'PRO.03.GLO.Fiabilidad': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242571339,
                            'row_id': 0
                        },                        
                    }
                },
                #CX
                'CX.01.GLO.Satisfacción': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242426121,
                            'row_id': 0
                        },                        
                    }
                },
                'CX.02.GLO.NPS': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242426120,
                            'row_id': 1654000667
                        },                        
                    }
                },
                'CX.03.GLO.Repetición': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242426128,
                            'row_id': 0
                        },                        
                    }
                },
                'CX.04.GLO.Dependencia': {
                    'surveymonkey_survey_ids': {
                        '168951300': {
                            'question_id': 242430114,
                            'row_id': 0
                        },                        
                    }
                },                                                                                                                                                                               
            }                
            for question_code in question_codes:
                question_code_item = question_codes[question_code]                        
                for surveymonkey_survey_id in question_code_item['surveymonkey_survey_ids']:
                    surveymonkey_survey_id_item = question_code_item['surveymonkey_survey_ids'][surveymonkey_survey_id]
                    
                    if surveymonkey_survey_id_item['row_id']==0:                                                                                
                        surveymonkey_survey_response_question_answer_ids = self.env['surveymonkey.survey.response.question.answer'].search(
                            [
                                ('datawarehouse_question_answer_id', '=', False),
                                ('surveymonkey_survey_response_id.status', '=', 'completed'),
                                ('surveymonkey_survey_response_id.survey_id', '=', surveymonkey_survey_id),
                                ('surveymonkey_question_id.question_id', '=', surveymonkey_survey_id_item['question_id'])
                            ]
                        )
                    else:
                        surveymonkey_survey_response_question_answer_ids = self.env['surveymonkey.survey.response.question.answer'].search(
                            [
                                ('datawarehouse_question_answer_id', '=', False),
                                ('surveymonkey_survey_response_id.status', '=', 'completed'),
                                ('surveymonkey_survey_response_id.survey_id', '=', surveymonkey_survey_id),
                                ('surveymonkey_question_id.question_id', '=', surveymonkey_survey_id_item['question_id']),
                                ('surveymonkey_question_row_id.row_id', '=', surveymonkey_survey_id_item['row_id'])
                            ]
                        )
                    
                    #operations
                    if len(surveymonkey_survey_response_question_answer_ids)>0:
                        cursor = return_connection['connection'].cursor()
                        
                        for surveymonkey_survey_response_question_answer_id in surveymonkey_survey_response_question_answer_ids:
                            datawarehouse_value = surveymonkey_survey_response_question_answer_id.surveymonkey_question_choice_id.datawarehouse_value
                            
                            if surveymonkey_survey_response_question_answer_id.surveymonkey_question_id.question_id=='242426120':
                                datawarehouse_value = datawarehouse_value/2
                            #insert
                            postgres_insert_query = """ INSERT INTO question_answer (company, code, create_date, value, value_int) VALUES (%s,%s,%s,%s,%s) returning id"""
                            record_to_insert = (
                                'OniAd', 
                                question_code, 
                                surveymonkey_survey_response_question_answer_id.surveymonkey_survey_response_id.date_modified, 
                                str(surveymonkey_survey_response_question_answer_id.surveymonkey_question_choice_id.text.encode('utf-8')), 
                                int(datawarehouse_value)                                
                            )
                            #_logger.info(record_to_insert)
                            cursor.execute(postgres_insert_query, record_to_insert)                                                                              
                            
                            return_connection['connection'].commit()
                            
                            return_id = cursor.fetchone()[0]
                            #_logger.info(return_id)
                            
                            surveymonkey_survey_response_question_answer_id.datawarehouse_question_answer_id = return_id
            #connect_close
            cursor = return_connection['connection'].cursor()
            cursor.close()
            return_connection['connection'].close()                                                                                                                                       
    
    @api.one    
    def process_answers(self, surveymonkey_survey_page_id=False, surveymonkey_question_id=False, answers=False):
        if surveymonkey_survey_page_id!=False and surveymonkey_question_id!=False and answers!=False:
            if len(answers)>0:
                for answer in answers:
                    #if need create row
                    surveymonkey_question_row_id = False
                    if 'row_id' in answer:
                        surveymonkey_question_row_ids = self.env['surveymonkey.question.row'].search([('row_id', '=', answer['row_id'])])
                        if len(surveymonkey_question_row_ids)>0:
                            surveymonkey_question_row_id = surveymonkey_question_row_ids[0].id                                                                                                                                                                                             
                    #if need create choice
                    surveymonkey_question_choice_id = False
                    if 'choice_id' in answer:
                        surveymonkey_question_choice_ids = self.env['surveymonkey.question.choice'].search([('choice_id', '=', answer['choice_id'])])
                        if len(surveymonkey_question_choice_ids)>0:
                            surveymonkey_question_choice_id = surveymonkey_question_choice_ids[0].id
                    #answer
                    surveymonkey_survey_response_question_answer_ids = self.env['surveymonkey.survey.response.question.answer'].search(
                        [
                            ('surveymonkey_survey_response_id', '=', self.id),
                            ('surveymonkey_survey_page_id', '=', surveymonkey_survey_page_id.id),
                            ('surveymonkey_question_id', '=', surveymonkey_question_id.id),
                            ('surveymonkey_question_row_id', '=', surveymonkey_question_row_id),
                            ('surveymonkey_question_choice_id', '=', surveymonkey_question_choice_id)                                                                
                        ]
                    )
                    if len(surveymonkey_survey_response_question_answer_ids)==0:
                        surveymonkey_survey_response_question_answer_vals = {
                            'surveymonkey_survey_response_id': self.id,
                            'surveymonkey_survey_page_id': surveymonkey_survey_page_id.id,
                            'surveymonkey_question_id': surveymonkey_question_id.id,
                            'surveymonkey_question_row_id': surveymonkey_question_row_id,
                            'surveymonkey_question_choice_id': surveymonkey_question_choice_id,                                                                                                                                                                                             
                        }
                        #if text is need
                        if 'text' in answer:
                            surveymonkey_survey_response_question_answer_vals['text'] = answer['text'] 
                                                
                        surveymonkey_survey_response_question_answer_obj = self.env['surveymonkey.survey.response.question.answer'].sudo().create(surveymonkey_survey_response_question_answer_vals)            
    
    @api.multi    
    def cron_oniad_surveymonkey_survey_responses(self, cr=None, uid=False, context=None):
        surveymonkey_web_service = SurveymonkeyWebService(self.env.user.company_id, self.env)
                
        oniad_surveymonkey_datawarehouse_survey_ids_need_check = self.env['ir.config_parameter'].sudo().get_param('oniad_surveymonkey_datawarehouse_survey_ids_need_check')
        survey_ids = oniad_surveymonkey_datawarehouse_survey_ids_need_check.split(',')        
        if len(survey_ids)>0:
            for survey_id in survey_ids:
                if survey_id!="":                                    
                    return_api_survey_responses = surveymonkey_web_service.get_survey_reponses(survey_id)                                    
                    if return_api_survey_responses['errors']==False:
                        #response                                
                        for response_item in return_api_survey_responses['response']:
                            if 'result' in response_item:
                                if response_item['result']['response_status']=='completed':
                                    #surveymonkey_survey_response
                                    surveymonkey_survey_response_vals = {
                                        'survey_id': response_item['result']['survey_id'],
                                        'response_id': response_item['id'],
                                        'collector_id': response_item['result']['collector_id'],
                                        'total_time': response_item['result']['total_time'],
                                        'status': response_item['result']['response_status'],
                                        'ip_address': response_item['result']['ip_address'],
                                        'date_modified': response_item['result']['date_modified'][:10]                                                                                                                                            
                                    }                                                                                                
                                    surveymonkey_survey_response_obj = self.env['surveymonkey.survey.response'].sudo().create(surveymonkey_survey_response_vals)
                                    #surveymonkey_survey_response_custom_variable
                                    if len(response_item['result']['custom_variables'])>0:
                                        for key,val in response_item['result']['custom_variables'].items():
                                            surveymonkey_survey_response_custom_variable_vals = {
                                                'surveymonkey_survey_response_id': surveymonkey_survey_response_obj.id,
                                                'field': key,
                                                'value': val                                                                                                                                                                                             
                                            }                        
                                            surveymonkey_survey_response_custom_variable_obj = self.env['surveymonkey.survey.response.custom.variable'].sudo().create(surveymonkey_survey_response_custom_variable_vals)
                                    #pages
                                    if 'pages' in response_item['result']:
                                        for page in response_item['result']['pages']:
                                            #if need create page
                                            surveymonkey_survey_page_id = False                                                                                                
                                            surveymonkey_survey_page_ids = self.env['surveymonkey.survey.page'].search([('page_id', '=', page['id'])])
                                            if len(surveymonkey_survey_page_ids)>0:
                                                surveymonkey_survey_page_id = surveymonkey_survey_page_ids[0]
                                            else:                                                
                                                return_api_survey_page = surveymonkey_web_service.get_survey_page(survey_id, page['id'])
                                                if return_api_survey_page['status_code']==200:
                                                    surveymonkey_survey_page_vals = {
                                                        'survey_id': response_item['result']['survey_id'],
                                                        'page_id': page['id'],
                                                        'title': return_api_survey_page['response']['title'],
                                                        'description': return_api_survey_page['response']['description'],
                                                        'position': return_api_survey_page['response']['position'],                                                                                                                                                                                             
                                                    }                        
                                                    surveymonkey_survey_page_obj = self.env['surveymonkey.survey.page'].sudo().create(surveymonkey_survey_page_vals)                                                
                                                    surveymonkey_survey_page_id = surveymonkey_survey_page_obj
                                            #questions
                                            for question in page['questions']:
                                                #if need create question
                                                surveymonkey_question_id = False
                                                surveymonkey_question_ids = self.env['surveymonkey.question'].search([('question_id', '=', question['id'])])
                                                if len(surveymonkey_question_ids)>0:
                                                    surveymonkey_question_id = surveymonkey_question_ids[0]
                                                else:
                                                    return_api_survey_page_question = surveymonkey_web_service.get_survey_page_question(survey_id, page['id'], question['id'])                                                    
                                                    if return_api_survey_page_question['status_code']==200:                                                
                                                        surveymonkey_question_vals = {
                                                            'question_id': question['id'],
                                                            'heading': '',
                                                            'position': return_api_survey_page_question['response']['position'],
                                                            'family': return_api_survey_page_question['response']['family'],
                                                            'subtype': return_api_survey_page_question['response']['subtype']                                                                                                                                                                                             
                                                        }
                                                        #headings
                                                        if 'headings' in return_api_survey_page_question['response']:
                                                            for heading in return_api_survey_page_question['response']['headings']:
                                                                surveymonkey_question_vals['heading'] = heading['heading']
                                                        #other                                                                                
                                                        surveymonkey_question_obj = self.env['surveymonkey.question'].sudo().create(surveymonkey_question_vals)
                                                        surveymonkey_question_id = surveymonkey_question_obj
                                                        
                                                        if 'answers' in return_api_survey_page_question['response']:
                                                            surveymonkey_question_obj.process_answers(return_api_survey_page_question['response']['answers'])                                                        
                                                #answers
                                                if 'answers' in question:
                                                    surveymonkey_survey_response_obj.process_answers(surveymonkey_survey_page_id, surveymonkey_question_id, question['answers'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                           