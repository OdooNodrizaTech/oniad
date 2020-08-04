# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
