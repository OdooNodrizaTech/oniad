# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SurveymonkeySurveyResponseCustomVariable(models.Model):
    _name = 'surveymonkey.survey.response.custom.variable'
    _description = 'Surveymonkey Survey Response Custom Variable'
    
    surveymonkey_survey_response_id = fields.Many2one(
        comodel_name='surveymonkey.survey.response',        
        string='Surveymonkey Survey Response'
    )
    field = fields.Char(        
        string='Survey Id'
    )
    value = fields.Char(        
        string='Response Id'
    )    
    survey_user_input_line_id = fields.Many2one(
        comodel_name='survey.user_input_line',        
        string='Survey User Input Line Id'
    )        