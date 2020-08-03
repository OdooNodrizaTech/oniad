# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models
import psycopg2
from ..surveymonkey.web_service import SurveymonkeyWebService
_logger = logging.getLogger(__name__)


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
                user=self.env['ir.config_parameter'].sudo().get_param(
                    'survey_oniad_datawarehouse_rds_user'
                ),
                password=self.env['ir.config_parameter'].sudo().get_param(
                    'survey_oniad_datawarehouse_rds_password'
                ),
                host=self.env['ir.config_parameter'].sudo().get_param(
                    'survey_oniad_datawarehouse_rds_endpoint'
                ),
                port="5432",
                database=self.env['ir.config_parameter'].sudo().get_param(
                    'survey_oniad_datawarehouse_rds_database'
                )
            )
            return {
                'connection': connection,
                'errors': False,
                'error': ''
            }
        except (psycopg2.Error) as error:
            return {
                'connection': False,
                'errors': True,
                'error': error
            }

    @api.model
    def cron_surveymonkey_survey_response_items_send_datawarehouse(self):
        # connect_postgresql_datawarehouse_rds
        return_connection = self.connect_postgresql_datawarehouse_rds()
        if return_connection['errors']:
            _logger.info(return_connection['error'])
        else:
            # question_codes
            question_codes = {
                # Atención al cliente
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
                # Producto
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
                # CX
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
                for survey_id in question_code_item['surveymonkey_survey_ids']:
                    survey_id_item = question_code_item[
                        'surveymonkey_survey_ids'
                    ][survey_id]
                    if survey_id_item['row_id'] == 0:
                        answer_ids = self.env[
                            'surveymonkey.survey.response.question.answer'
                        ].search(
                            [
                                ('datawarehouse_question_answer_id', '=', False),
                                (
                                    'surveymonkey_survey_response_id.status',
                                    '=',
                                    'completed')
                                ,
                                (
                                    'surveymonkey_survey_response_id.survey_id',
                                    '=',
                                    survey_id
                                ),
                                (
                                    'surveymonkey_question_id.question_id',
                                    '=',
                                    survey_id_item['question_id']
                                )
                            ]
                        )
                    else:
                        answer_ids = self.env[
                            'surveymonkey.survey.response.question.answer'
                        ].search(
                            [
                                ('datawarehouse_question_answer_id', '=', False),
                                (
                                    'surveymonkey_survey_response_id.status',
                                    '=',
                                    'completed'
                                ),
                                (
                                    'surveymonkey_survey_response_id.survey_id',
                                    '=',
                                    survey_id
                                ),
                                (
                                    'surveymonkey_question_id.question_id',
                                    '=',
                                    survey_id_item['question_id']
                                ),
                                (
                                    'surveymonkey_question_row_id.row_id',
                                    '=',
                                    survey_id_item['row_id']
                                )
                            ]
                        )
                    
                    # operations
                    if answer_ids:
                        cursor = return_connection['connection'].cursor()
                        
                        for answer_id in answer_ids:
                            answer_id_sq = answer_id.surveymonkey_question_id
                            answer_id_sqc = \
                                answer_id.surveymonkey_question_choice_id
                            answer_id_ssr = \
                                answer_id.surveymonkey_survey_response_id
                            datawarehouse_value = answer_id_sqc.datawarehouse_value
                            
                            if answer_id_sq.question_id == '242426120':
                                datawarehouse_value = datawarehouse_value/2
                            # insert
                            postgres_insert_query = """
                            INSERT INTO question_answer 
                            (company, code, create_date, value, value_int) 
                            VALUES (%s,%s,%s,%s,%s) returning id
                            """
                            record_to_insert = (
                                'OniAd', 
                                question_code, 
                                answer_id_ssr.date_modified,
                                str(answer_id_sqc.text.encode('utf-8')),
                                int(datawarehouse_value)                                
                            )
                            # _logger.info(record_to_insert)
                            cursor.execute(
                                postgres_insert_query,
                                record_to_insert
                            )
                            return_connection['connection'].commit()
                            return_id = cursor.fetchone()[0]
                            # _logger.info(return_id)
                            answer_id.datawarehouse_question_answer_id = \
                                return_id
            # connect_close
            cursor = return_connection['connection'].cursor()
            cursor.close()
            return_connection['connection'].close()                                                                                                                                       
    
    @api.multi
    def process_answers(self,
                        page_id=False,
                        question_id=False,
                        answers=False
                        ):
        self.ensure_one()
        if page_id and question_id and answers:
            if len(answers) > 0:
                for answer in answers:
                    # if need create row
                    question_row_id = False
                    if 'row_id' in answer:
                        question_row_ids = self.env[
                            'surveymonkey.question.row'
                        ].search(
                            [
                                ('row_id', '=', answer['row_id'])
                            ]
                        )
                        if question_row_ids:
                            question_row_id = question_row_ids[0]
                    # if need create choice
                    question_choice_id = False
                    if 'choice_id' in answer:
                        question_choice_ids = self.env[
                            'surveymonkey.question.choice'
                        ].search(
                            [
                                ('choice_id', '=', answer['choice_id'])
                            ]
                        )
                        if question_choice_ids:
                            question_choice_id = question_choice_ids[0]
                    # answer
                    answer_ids = self.env[
                        'surveymonkey.survey.response.question.answer'
                    ].search(
                        [
                            (
                                'surveymonkey_survey_response_id',
                                '=',
                                self.id
                            ),
                            (
                                'surveymonkey_survey_page_id',
                                '=',
                                page_id.id
                            ),
                            (
                                'surveymonkey_question_id',
                                '=',
                                question_id.id
                            ),
                            (
                                'surveymonkey_question_row_id',
                                '=',
                                question_row_id.id
                            ),
                            (
                                'surveymonkey_question_choice_id',
                                '=',
                                question_choice_id.id
                            )
                        ]
                    )
                    if len(answer_ids) == 0:
                        vals = {
                            'surveymonkey_survey_response_id':
                                self.id,
                            'surveymonkey_survey_page_id':
                                page_id.id,
                            'surveymonkey_question_id':
                                question_id.id,
                            'surveymonkey_question_row_id':
                                question_row_id.id,
                            'surveymonkey_question_choice_id':
                                question_choice_id.id,
                        }
                        #if text is need
                        if 'text' in answer:
                            vals['text'] = answer['text']
                                                
                        self.env[
                            'surveymonkey.survey.response.question.answer'
                        ].sudo().create(vals)
    
    @api.model    
    def cron_oniad_surveymonkey_survey_responses(self):
        surveymonkey_web_service = SurveymonkeyWebService(
            self.env.user.company_id,
            self.env
        )
        ids_need_check = self.env['ir.config_parameter'].sudo().get_param(
            'oniad_surveymonkey_datawarehouse_survey_ids_need_check'
        )
        survey_ids = ids_need_check.split(',')
        if len(survey_ids) > 0:
            for survey_id in survey_ids:
                if survey_id != "":
                    res = surveymonkey_web_service.get_survey_reponses(
                        survey_id
                    )
                    if not res['errors']:
                        # response
                        for response_item in res['response']:
                            if 'result' in response_item:
                                if response_item['result']['response_status'] == 'completed':
                                    # surveymonkey_survey_response
                                    vals = {
                                        'survey_id':
                                            response_item['result']['survey_id'],
                                        'response_id': response_item['id'],
                                        'collector_id':
                                            response_item['result']['collector_id'],
                                        'total_time':
                                            response_item['result']['total_time'],
                                        'status':
                                            response_item['result']['response_status'],
                                        'ip_address':
                                            response_item['result']['ip_address'],
                                        'date_modified':
                                            response_item['result']['date_modified'][:10]
                                    }                                                                                                
                                    response_obj = self.env[
                                        'surveymonkey.survey.response'
                                    ].sudo().create(vals)
                                    # surveymonkey_survey_response_custom_variable
                                    if len(response_item['result']['custom_variables']) > 0:
                                        res_id_cv = response_item['result']['custom_variables']
                                        for key, val in res_id_cv.items():
                                            vals = {
                                                'surveymonkey_survey_response_id':
                                                    response_obj.id,
                                                'field': key,
                                                'value': val                                                                                                                                                                                             
                                            }                        
                                            self.env[
                                                'surveymonkey.survey.response.custom.variable'
                                            ].sudo().create(vals)
                                    # pages
                                    if 'pages' in response_item['result']:
                                        for page in response_item['result']['pages']:
                                            # if need create page
                                            page_id = False
                                            page_ids = self.env[
                                                'surveymonkey.survey.page'
                                            ].search(
                                                [
                                                    ('page_id', '=', page['id'])
                                                ]
                                            )
                                            if page_ids:
                                                page_id = page_ids[0]
                                            else:                                                
                                                res_page = surveymonkey_web_service.get_survey_page(
                                                    survey_id,
                                                    page['id']
                                                )
                                                if res_page['status_code'] == 200:
                                                    vals = {
                                                        'survey_id':
                                                            response_item['result']['survey_id'],
                                                        'page_id': page['id'],
                                                        'title': res_page['response']['title'],
                                                        'description':
                                                            res_page['response']['description'],
                                                        'position':
                                                            res_page['response']['position'],
                                                    }                        
                                                    page_obj = self.env[
                                                        'surveymonkey.survey.page'
                                                    ].sudo().create(vals)
                                                    surveymonkey_survey_page_id = page_obj
                                            # questions
                                            for question in page['questions']:
                                                # if need create question
                                                question_id = False
                                                question_ids = self.env[
                                                    'surveymonkey.question'
                                                ].search(
                                                    [
                                                        ('question_id', '=', question['id'])
                                                    ]
                                                )
                                                if question_ids:
                                                    question_id = question_ids[0]
                                                else:
                                                    res_page_question = surveymonkey_web_service.get_survey_page_question(
                                                        survey_id,
                                                        page['id'],
                                                        question['id']
                                                    )
                                                    if return_api_survey_page_question['status_code'] == 200:
                                                        vals = {
                                                            'question_id': question['id'],
                                                            'heading': '',
                                                            'position':
                                                                res_page_question['response']['position'],
                                                            'family':
                                                                res_page_question['response']['family'],
                                                            'subtype':
                                                                res_page_question['response']['subtype']
                                                        }
                                                        # headings
                                                        if 'headings' in res_page_question['response']:
                                                            rpq_response = res_page_question['response']
                                                            for heading in rpq_response['headings']:
                                                                vals['heading'] = heading['heading']
                                                        # other
                                                        question_obj = self.env[
                                                            'surveymonkey.question'
                                                        ].sudo().create(vals)
                                                        surveymonkey_question_id = question_obj
                                                        if 'answers' in res_page_question['response']:
                                                            question_obj.process_answers(
                                                                res_page_question['response']['answers']
                                                            )
                                                # answers
                                                if 'answers' in question:
                                                    surveymonkey_survey_response_obj.process_answers(
                                                        page_id,
                                                        question_id,
                                                        question['answers']
                                                    )
