# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SurveymonkeySurveyPage(models.Model):
    _name = 'surveymonkey.survey.page'
    _description = 'Surveymonkey Survey Page'

    survey_id = fields.Char(
        string='Id'
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
        string='Survey Page Id'
    )

    @api.model
    def cron_oniad_surveymonkey_generate_odoo_surveis(self):
        # surveymonkye.survey.page
        page_ids = self.env['surveymonkey.survey.page'].search(
            [
                ('survey_survey_id', '=', False),
                ('survey_page_id', '=', False)
            ]
        )
        if page_ids:
            for page_id in page_ids:
                # survey_survey
                if page_id.survey_survey_id.id == 0:
                    page_ids2 = self.env['surveymonkey.survey.page'].search(
                        [
                            ('survey_survey_id', '!=', False),
                            ('survey_id', '=', page_id.survey_id)
                        ]
                    )
                    if len(page_ids2) == 0:
                        vals = {
                            'active': True,
                            'is_closed': False,
                            'title': page_id.title,
                            'users_can_go_back': False
                        }
                        survey_obj = self.env['survey.survey'].sudo().create(vals)
                        page_id.survey_survey_id = survey_obj.id
                    else:
                        page_id.survey_survey_id = page_ids2[0].survey_survey_id.id
                # survey_page
                if page_id.survey_page_id.id == 0:
                    survey_page_ids = self.env['survey.page'].search(
                        [
                            ('survey_id', '=', page_id.survey_survey_id.id)
                        ]
                    )
                    vals = {
                        'title': page_id.title,
                        'survey_id': page_id.survey_survey_id.id,
                        'sequence': len(survey_page_ids)
                    }
                    survey_page_obj = self.env['survey.page'].sudo().create(
                        vals
                    )
                    page_id.survey_page_id = survey_page_obj.id
        # surveymonkey.survey.response
        response_ids = self.env['surveymonkey.survey.response'].search(
            [
                ('survey_user_input_id', '=', False),
                ('status', '=', 'completed')
            ]
        )
        if response_ids:
            for response_id in response_ids:
                page_ids = self.env['surveymonkey.survey.page'].search(
                    [
                        ('survey_id', '=', response_id.survey_id)
                    ]
                )
                if page_ids:
                    page_id = page_ids[0]
                    vals = {
                        'date_create': response_id.date_modified,
                        'email': response_id.ip_address,
                        'state': 'done',
                        'survey_id': page_id.survey_survey_id.id,
                        'type': 'manually'
                    }
                    user_input_obj = self.env['survey.user_input'].sudo().create(
                        vals
                    )
                    response_id.survey_user_input_id = user_input_obj.id
        # surveymonkey.survey.response.custom.variable
        variable_ids = self.env['surveymonkey.survey.response.custom.variable'].search(
            [
                ('survey_user_input_line_id', '=', False)
            ]
        )
        if variable_ids:
            for variable_id in variable_ids:
                variable_id_ssr = variable_id.surveymonkey_survey_response_id
                user_input_id = variable_id_ssr.survey_user_input_idd
                page_id = user_input_id.survey_id.page_ids[0].id
                survey_id = user_input_id.survey_id.id
                survey_question_ids = self.env['survey.question'].search(
                    [
                        ('survey_id', '=', survey_id),
                        ('question', '=', str(variable_id.field))
                    ]
                )
                if len(survey_question_ids) == 0:
                    survey_question_ids2 = self.env['survey.question'].search(
                        [
                            ('page_id', '=', page_id)
                        ]
                    )
                    vals = {
                        'page_id': page_id,
                        'question': str(variable_id.field),
                        'type': 'free_text',
                        'sequence': len(survey_question_ids2)
                    }
                    self.env['survey.question'].sudo().create(vals)
                else:
                    vals = {
                        'page_id': page_id,
                        'question_id': survey_question_ids[0].id,
                        'survey_id': survey_id,
                        'user_input_id': user_input_id.id,
                        'value_free_text': variable_id.value,
                        'answer_type': 'free_text'
                    }
                    input_line_obj = self.env[
                        'survey.user_input_line'
                    ].sudo().create(vals)
                    variable_id.survey_user_input_line_id = input_line_obj.id
        # surveymonkey.survey.response.question.answer
        answer_ids = self.env[
            'surveymonkey.survey.response.question.answer'
        ].search(
            [('survey_user_input_line_id', '=', False)
             ]
        )
        if answer_ids:
            for answer_id in answer_ids:

                answer_id_ssp = answer_id.surveymonkey_survey_page_id.survey_page_id
                answer_id_ssr = answer_id.surveymonkey_survey_response_id
                answer_id_sq = answer_id.surveymonkey_question_id
                answer_id_sqc = answer_id.surveymonkey_question_choice_id

                survey_id = answer_id_ssr.survey_user_input_id.survey_id.id
                user_input_id = answer_id_ssr.survey_user_input_id.id

                if answer_id_sq.survey_question_id.id == 0:
                    question_type = None
                    if answer_id_sq.family == 'open_ended' \
                            and answer_id_sq.subtype == 'essay':
                        question_type = 'free_text'
                    elif answer_id_sq.family == 'matrix' \
                            and answer_id_sq.subtype == 'rating':
                        question_type = 'matrix'
                    elif answer_id_sq.family == 'single_choice':
                        question_type = 'simple_choice'

                    if question_type is not None:
                        vals = {
                            'page_id': answer_id_ssp.id,
                            'question': str(answer_id_sq.heading.encode('utf-8')),
                            'type': question_type,
                            'sequence': answer_id_sq.position
                        }
                        survey_question_obj = self.env[
                            'survey.question'
                        ].sudo().create(vals)
                        answer_id.surveymonkey_question_id.survey_question_id = \
                            survey_question_obj.id
                        # labels
                        if question_type == 'matrix':
                            # label_ids (choice)
                            choice_ids = self.env[
                                'surveymonkey.question.choice'
                            ].search(
                                [
                                    (
                                        'surveymonkey_question_id',
                                        '=',
                                        answer_id_sq.id
                                    )
                                ]
                            )
                            if choice_ids:
                                for choice_id in choice_ids:
                                    vals = {
                                        'value': choice_id.text,
                                        'question_id':
                                            answer_id_sq.survey_question_id.id,
                                        'sequence': choice_id.position
                                    }
                                    label_obj = self.env[
                                        'survey.label'
                                    ].sudo().create(vals)
                                    choice_id.survey_label_id = label_obj.id
                            # label_ids_2 (row)
                            row_ids = self.env['surveymonkey.question.row'].search(
                                [
                                    (
                                        'surveymonkey_question_id',
                                        '=',
                                        answer_id_sq.id
                                    )
                                ]
                            )
                            if row_ids:
                                for row_id in row_ids:
                                    row_id_sq = row_id.surveymonkey_question_id
                                    vals = {
                                        'value': row_id.text,
                                        'question_id_2':
                                            row_id_sq.survey_question_id.id,
                                        'sequence': row_id.position
                                    }
                                    label_obj = self.env[
                                        'survey.label'
                                    ].sudo().create(vals)
                                    row_id.survey_label_id = label_obj.id
                        elif question_type == 'simple_choice':
                            # label_ids (choice)
                            choice_ids = self.env[
                                'surveymonkey.question.choice'
                            ].search(
                                [
                                    (
                                        'surveymonkey_question_id',
                                        '=',
                                        answer_id_sq.id
                                    )
                                ]
                            )
                            if choice_ids:
                                for choice_id in choice_ids:
                                    vals = {
                                        'value': choice_id.text,
                                        'question_id':
                                            choice_id.survey_question_id.id,
                                        'sequence': choice_id.position
                                    }
                                    label_obj = self.env[
                                        'survey.label'
                                    ].sudo().create(vals)
                                    choice_id.survey_label_id = label_obj.id
                else:
                    question_type = str(answer_id_sq.survey_question_id.type)
                    vals = {
                        'page_id': answer_id_ssp.id,
                        'question_id':
                            answer_id_sq.survey_question_id.id,
                        'survey_id': survey_id,
                        'user_input_id': user_input_id,
                        'answer_type': 'suggestion'
                    }
                    if question_type == 'free_text':
                        vals['value_free_text'] = str(answer_id.text.encode('utf-8'))
                        vals['answer_type'] = question_type
                    elif question_type == 'simple_choice':
                        vals['value_suggested'] = answer_id_sqc.survey_label_id.id
                    elif question_type == 'matrix':
                        vals['value_suggested'] = answer_id_sqc.survey_label_id.id
                        vals['value_suggested_row'] = \
                            answer_id.surveymonkey_question_row_id.survey_label_id.id
                    input_line_obj = self.env[
                        'survey.user_input_line'
                    ].sudo().create(vals)
                    answer_id.survey_user_input_line_id = input_line_obj.id
        # define partner_id
        user_input_ids = self.env['survey.user_input'].search(
            [
                ('partner_id', '=', False)
            ]
        )
        if user_input_ids:
            for user_input_id in user_input_ids:
                question_ids = self.env['survey.question'].search(
                    [
                        ('survey_id', '=', user_input_id.survey_id.id),
                        ('question', '=', 'partner_id'),
                    ]
                )
                if question_ids:
                    question_id = question_ids[0]
                    # get partner_id
                    user_input_line_ids = self.env[
                        'survey.user_input_line'
                    ].search(
                        [
                            ('user_input_id', '=', user_input_id.id),
                            ('question_id', '=', question_id.id)
                        ]
                    )
                    if user_input_line_ids:
                        user_input_line_id = user_input_line_ids[0]
                        partner_ids = self.env['res.partner'].search(
                            [
                                ('id', '=', user_input_line_id.partner_id.id)
                            ]
                        )
                        if partner_ids:
                            user_input_id.partner_id = partner_ids[0].id
                else:
                    question_ids = self.env['survey.question'].search(
                        [
                            ('survey_id', '=', user_input_id.survey_id.id),
                            ('question', '=', 'oniad_user_id'),
                        ]
                    )
                    if question_ids:
                        question_id = question_ids[0]
                        # get oniad_user_id
                        user_input_line_ids = self.env[
                            'survey.user_input_line'
                        ].search(
                            [
                                ('user_input_id', '=', user_input_id.id),
                                ('question_id', '=', question_id.id)
                            ]
                        )
                        if user_input_line_ids:
                            user_input_line_id = user_input_line_ids[0]
                            partner_ids = self.env['res.partner'].search(
                                [
                                    (
                                        'oniad_user_id',
                                        '=',
                                        user_input_line_id.oniad_user_id.id
                                    )
                                ]
                            )
                            if partner_ids:
                                user_input_id.partner_id = partner_ids[0].id
