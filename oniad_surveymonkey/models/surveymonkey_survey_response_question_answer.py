# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SurveymonkeySurveyResponseQuestionAnswer(models.Model):
    _name = 'surveymonkey.survey.response.question.answer'
    _description = 'Surveymonkey Survey Response Question Answer'
                       
    surveymonkey_survey_response_id = fields.Many2one(
        comodel_name='surveymonkey.survey.response',        
        string='Surveymonkey Survey Response'
    )
    surveymonkey_survey_page_id = fields.Many2one(
        comodel_name='surveymonkey.survey.page',        
        string='Surveymonkey Survey Page'
    )
    surveymonkey_question_id = fields.Many2one(
        comodel_name='surveymonkey.question',        
        string='Surveymonkey Question'
    )
    surveymonkey_question_row_id = fields.Many2one(
        comodel_name='surveymonkey.question.row',        
        string='Surveymonkey Question Row'
    )
    surveymonkey_question_choice_id = fields.Many2one(
        comodel_name='surveymonkey.question.choice',        
        string='Surveymonkey Question Choice'
    )
    text = fields.Text(        
        string='Row Id'
    )
    datawarehouse_question_answer_id = fields.Integer(        
        string='Datawarehouse Question Answer Id',
    )
    survey_user_input_line_id = fields.Many2one(
        comodel_name='survey.user_input_line',        
        string='Survey User Input Line Id'
    )                