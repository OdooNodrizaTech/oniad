# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveymonkeyQuestion(models.Model):
    _name = 'surveymonkey.question'
    _description = 'Surveymonkey Question'
    
    question_id = fields.Char(        
        string='Question Id'
    )
    heading = fields.Char(        
        string='Heading'
    )
    position = fields.Integer(        
        string='Position'
    )        
    family = fields.Selection(
        selection=[
            ('single_choice','Single Choice'), 
            ('multiple_choice','Multiple Choice'), 
            ('matrix','Matrix'), 
            ('open_ended','Open Ended'), 
            ('demographic','Demographic'), 
            ('datetime','Datetime'), 
            ('presentation','Presentation')
        ],
        string='Family'
    )
    subtype = fields.Selection(
        selection=[
            ('vertical','Vertical'),
            ('vertical_two_col','Vertical Two Col'),             
            ('single','Single'),
            ('essay','Essay'),             
            ('rating','Rating'), 
            ('ranking','Ranking'), 
            ('menu','Menu'), 
            ('multi','Multi'), 
            ('numerical','Numerical'),
            ('international','International'),
            ('both','Both'),
            ('image','Image')
        ],
        string='Subtype'
    )
    survey_question_id = fields.Many2one(
        comodel_name='survey.question',        
        string='Survey Question Id'
    )
    
    @api.one    
    def process_answers(self, answers=False):
        if answers!=False:
            if 'rows' in answers:
                for row in answers['rows']:
                    surveymonkey_question_row_ids = self.env['surveymonkey.question.row'].search([('row_id', '=', row['id'])])
                    if len(surveymonkey_question_row_ids)==0:
                        surveymonkey_question_row_vals = {
                            'row_id': row['id'],
                            'surveymonkey_question_id': self.id,
                            'position': row['position'],
                            'text': row['text']                                                                                                                                                                                             
                        }                        
                        surveymonkey_question_row_obj = self.env['surveymonkey.question.row'].sudo().create(surveymonkey_question_row_vals)
            #choices
            if 'choices' in answers:
                for choice in answers['choices']:
                    surveymonkey_question_choice_ids = self.env['surveymonkey.question.choice'].search([('choice_id', '=', choice['id'])])
                    if len(surveymonkey_question_choice_ids)==0:
                        surveymonkey_question_choice_vals = {
                            'choice_id': choice['id'],
                            'surveymonkey_question_id': self.id,
                            'position': choice['position'],
                            'text': choice['text'],
                            'description': ''                                                                                      
                        }
                        #description
                        if 'description' in choice:
                            surveymonkey_question_choice_vals['description'] = choice['description']
                                                
                        surveymonkey_question_choice_obj = self.env['surveymonkey.question.choice'].sudo().create(surveymonkey_question_choice_vals)