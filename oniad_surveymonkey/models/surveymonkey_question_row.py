# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveymonkeyQuestionRow(models.Model):
    _name = 'surveymonkey.question.row'
    _description = 'Surveymonkey Question Row'
            
    row_id = fields.Char(        
        string='Row Id'
    )
    surveymonkey_question_id = fields.Many2one(
        comodel_name='surveymonkey.question',        
        string='Surveymonkey Question'
    )    
    position = fields.Text(        
        string='Position'
    )
    text = fields.Text(        
        string='Row Id'
    )
    survey_label_id = fields.Many2one(
        comodel_name='survey.label',        
        string='Survey Label Id'
    )                