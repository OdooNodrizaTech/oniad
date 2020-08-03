# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import tools
import requests
_logger = logging.getLogger(__name__)


class SurveymonkeyWebService():

    def __init__(self, company, env):
        self.company = company
        self.custom_env = env
                            
        self.api_access_token = tools.config.get(
            'surveymonkey_api_access_token'
        )
        self.api_version = env['ir.config_parameter'].sudo().get_param(
            'oniad_surveymonkey_api_version'
        )
        self.url_api = 'https://api.surveymonkey.net'
    
    # slack_message_error
    def sack_message_error(self, text, endpoint):
        slack_message_attachments = [
            {                    
                "title": 'Error API Surveymonkey',
                "text": text,                         
                "color": "#ff0000",
                "fields": [                    
                    {
                        "title": "Endpoint",
                        "value": endpoint
                    }
                ]                                                                                                        
            }
        ]        
        slack_message_vals = {
            'attachments': slack_message_attachments,
            'channel': self.custom_env['ir.config_parameter'].sudo().get_param(
                'slack_oniad_log_channel'
            )
        }                        
        self.custom_env['slack.message'].sudo().create(slack_message_vals)
    
    # api
    def get_survey_page(self, survey_id, page_id):
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = '%/%s/surveys/%s/pages/%s' % (
            self.url_api,
            self.api_version,
            survey_id,
            page_id
        )
        response = client.get(uri, headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(
                        response_json['error']['message'],
                        uri
                    )
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
        
    # api
    def get_survey_page_question(self, survey_id, page_id, question_id):
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = '%/%s/surveys/%s/pages/%s/questions/%s' % (
            self.url_api,
            self.api_version,
            survey_id,
            page_id,
            question_id
        )
        response = client.get(uri, headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(
                        response_json['error']['message'],
                        uri
                    )
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    # api
    def get_survey_reponse_details(self, survey_id, response_id):
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = '%s/%s/surveys/%s/responses/%s/details' % (
            self.url_api,
            self.api_version,
            survey_id,
            response_id
        )
        response = client.get(uri, headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(
                        response_json['error']['message'],
                        uri
                    )
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    # api
    def get_survey_reponses_real(self, survey_id, page=1, per_page=50):
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = '%s/%s/surveys/%s/responses?page=%s&per_page=%s' % (
            self.url_api,
            self.api_version,
            survey_id,
            page,
            per_page
        )
        response = client.get(uri, headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(
                        response_json['error']['message'],
                        uri
                    )
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    
    def get_survey_reponses(self, survey_id, per_page=50):
        response = {
            'errors': True, 
            'error': "",
            'status_code': "",
            'response': [] 
        }
        response_api = self.get_survey_reponses_real(
            survey_id,
            1,
            per_page
        )
        if response_api['status_code'] != 200:
            if 'error' in response_api['response']:
                if 'message' in response_api['response']['error']:
                    response['error'] = response_api['response']['error']['message']                                                                                        
        else:
            response['errors'] = False
            response['response'].extend(response_api['response']['data'])
            # Fix need other pages
            pages_calculate = float(response_api['response']['total'])/float(response_api['response']['per_page'])
            pages_calculate = "{0:.2f}".format(pages_calculate)
            pages_calculate_split = pages_calculate.split('.')
            if pages_calculate_split[1] != "00":
                pages_calculate = int(pages_calculate_split[0])+1
                                        
            if pages_calculate > 1:
                for i in range(2, pages_calculate+1):
                    response_page = self.get_survey_reponses_real(
                        survey_id,
                        i,
                        response_api['response']['per_page']
                    )
                    if response_page['status_code'] == 200:
                        if 'data' in response_page['response']:
                                                    
                            response['response'].extend(response_page['response']['data'])
            # fix response
            response_pre = response['response']
            response['response'] = []
            # create_array
            survey_response_ids_custom = []
            survey_response_ids = self.custom_env['surveymonkey.survey.response'].search(
                [
                    ('survey_id', '=', survey_id)
                ]
            )
            if survey_response_ids:
                for response_id in survey_response_ids:
                    survey_response_ids_custom.append(response_id.response_id)

            for response_item in response_pre:
                if response_item['id'] not in survey_response_ids_custom:
                    response_item_params = {
                        'id': response_item['id'],
                        'result': "",
                    }
                    res_response_api = self.get_survey_reponse_details(
                        survey_id,
                        response_item['id']
                    )
                    if res_response_api['status_code'] == 200:
                        response_item_params['result'] = res_response_api['response']
                    
                    response['response'].append(response_item_params)
        # return
        return response
        
    def get_api_survey_reponses(self, endpoint):
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = "%s%s" % (
            self.url_api,
            endpoint
        )
        client_response = client.get(uri, headers=headers)
        if client_response.status_code == 200:
            return client_response.json()
        else:
            return False
    
    # api
    def get_survey_reponse(self, survey_id, response_id):
        client = requests.session()

        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = '%s/%s/surveys/%s/responses/%s' % (
            self.url_api,
            self.api_version,
            survey_id,
            response_id
        )
        response = client.get(uri, headers=headers)
        response_json = response.json()
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    # api
    def get_surveys(self):
        response = {
            'errors': True, 
            'error': "",
            'status_code': "",
            'response': "" 
        }
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = "%s/%s/surveys" % (
            self.url_api,
            self.api_version
        )
        client_response = client.get(uri, headers=headers)
        client_response_json = client_response.json()
        response['status_code'] = client_response.status_code
        if response['status_code'] == 200:
            response['errors'] = False
            response['response'] = client_response_json
        else:
            if 'error' in client_response_json:
                if 'message' in client_response_json['error']:
                    response['error'] = client_response_json['error']['message']                    
                    self.sack_message_error(
                        response['error'],
                        uri
                    )
        return response
    
    # api
    def get_users_me(self):
        response = {
            'errors': True, 
            'error': "",
            'status_code': "",
            'response': "" 
        }
        client = requests.session()
        headers = {
            "Authorization": "bearer %s" % self.api_access_token,
            "Content-Type": "application/json"
        }
        uri = "%s/%s/users/me" % (
            self.url_api,
            self.api_version
        )
        client_response = client.get(uri, headers=headers)
        client_response_json = client_response.json()
        response['status_code'] = client_response.status_code
        if response['status_code'] == 200:
            response['errors'] = False
            response['response'] = client_response_json
        else:
            if 'error' in client_response_json:
                if 'message' in client_response_json['error']:
                    response['error'] = client_response_json['error']['message']                    
                    self.sack_message_error(
                        response['error'],
                        uri
                    )
        return response
