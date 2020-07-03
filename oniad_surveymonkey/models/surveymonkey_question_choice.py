# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveymonkeyQuestionChoice(models.Model):
    _name = 'surveymonkey.question.choice'
    _description = 'Surveymonkey Question Choice'
            
    choice_id = fields.Char(        
        string='Choice Id'
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
    description = fields.Text(        
        string='Description'
    )
    datawarehouse_value = fields.Integer(        
        string='Datawarehouse Value'
    )
    survey_label_id = fields.Many2one(
        comodel_name='survey.label',        
        string='Survey Label Id'
    )    