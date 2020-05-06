# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models, tools
import datetime, os, codecs, pysftp
from dateutil.relativedelta import relativedelta

import requests

class SurveymonkeyWebService():

    def __init__(self, company, env):
        self.company = company
        self.custom_env = env
                            
        self.api_access_token = tools.config.get('surveymonkey_api_access_token')        
        self.api_version = env['ir.config_parameter'].sudo().get_param('oniad_surveymonkey_api_version')                        
    
    #slack_message_error
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
            'channel': self.custom_env['ir.config_parameter'].sudo().get_param('slack_oniad_log_channel')                                                                                                                 
        }                        
        slack_message_obj = self.custom_env['slack.message'].sudo().create(slack_message_vals)    
    
    #api
    def get_survey_page(self, survey_id, page_id):
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/surveys/"+str(survey_id)+'/pages/'+str(page_id)        
        uri = "%s%s" % (HOST, ENDPOINT)
        
        response = client.get(uri, headers=headers)
        response_json = response.json()
        
        if response.status_code!=200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(response_json['error']['message'], ENDPOINT)#Slack_message_error
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
        
    #api
    def get_survey_page_question(self, survey_id, page_id, question_id):
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/surveys/"+str(survey_id)+'/pages/'+str(page_id)+'/questions/'+str(question_id)        
        uri = "%s%s" % (HOST, ENDPOINT)
        
        response = client.get(uri, headers=headers)
        response_json = response.json()
        
        if response.status_code!=200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(response_json['error']['message'], ENDPOINT)#Slack_message_error
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    #api
    def get_survey_reponse_details(self, survey_id, response_id):
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/surveys/"+str(survey_id)+'/responses/'+str(response_id)+'/details'        
        uri = "%s%s" % (HOST, ENDPOINT)
        
        response = client.get(uri, headers=headers)
        response_json = response.json()
        
        if response.status_code!=200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(response_json['error']['message'], ENDPOINT)#Slack_message_error
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    #api
    def get_survey_reponses_real(self, survey_id, page=1, per_page=50):
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/surveys/"+str(survey_id)+'/responses?page='+str(page)+'&per_page='+str(per_page)        
        uri = "%s%s" % (HOST, ENDPOINT)
        #_logger.info(uri)
        
        response = client.get(uri, headers=headers)
        response_json = response.json()
        
        if response.status_code!=200:
            if 'error' in response_json:
                if 'message' in response_json['error']:        
                    self.sack_message_error(response_json['error']['message'], ENDPOINT)#Slack_message_error
        
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
        
        response_api = self.get_survey_reponses_real(survey_id, 1, per_page)
        
        if response_api['status_code']!=200:
            if 'error' in response_api['response']:
                if 'message' in response_api['response']['error']:
                    response['error'] = response_api['response']['error']['message']                                                                                        
        else:
            response['errors'] = False
            response['response'].extend(response_api['response']['data'])
            #Fix need other pages
            total_pages_calculate = float(response_api['response']['total'])/float(response_api['response']['per_page'])
            total_pages_calculate = "{0:.2f}".format(total_pages_calculate)
            total_pages_calculate_split = total_pages_calculate.split('.')
            if total_pages_calculate_split[1]!="00":
                total_pages_calculate = int(total_pages_calculate[0])+1
                                        
            if total_pages_calculate>1:                                                                                                                
                for i in range(2, total_pages_calculate+1):                            
                    response_page = self.get_survey_reponses_real(survey_id, i, response_api['response']['per_page'])
                    if response_page['status_code']==200:
                        if 'data' in response_page['response']:
                                                    
                            response['response'].extend(response_page['response']['data'])
            #fix response
            response_pre = response['response']
            response['response'] = []
            #create_array
            surveymonkey_survey_response_ids_custom = []
            surveymonkey_survey_response_ids = self.custom_env['surveymonkey.survey.response'].search([('survey_id', '=', survey_id)])
            if len(surveymonkey_survey_response_ids)>0:
                for surveymonkey_survey_response_id in surveymonkey_survey_response_ids:
                    surveymonkey_survey_response_ids_custom.append(surveymonkey_survey_response_id.response_id)
            
            
            for response_item in response_pre:
                #_logger.info(response_item)
                #_logger.info(response_item['id'])
                                
                if response_item['id'] not in surveymonkey_survey_response_ids_custom:#fix not previously created                
                    response_item_params = {
                        'id':response_item['id'],
                        'result': "",
                    }
                    #response_survey_response_api = self.get_survey_reponse(survey_id, response_item['id'])
                    response_details_survey_response_api = self.get_survey_reponse_details(survey_id, response_item['id'])
                    if response_details_survey_response_api['status_code']==200:
                        response_item_params['result'] = response_details_survey_response_api['response']                                        
                    
                    response['response'].append(response_item_params)                    
                #_logger.info(response_survey_response_api)                                             
        
        #_logger.info(response)
                                        
        return response
        
    def get_api_survey_reponses(self, endpoint):
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"        
        uri = "%s%s" % (HOST, endpoint)
        
        client_response = client.get(uri, headers=headers)
        client_response_json = client_response.json()
        
        if client_response.status_code==200:
            return client_response_json
        else:
            return False            
                    
    
    #api
    def get_survey_reponse(self, survey_id, response_id):
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/surveys/"+str(survey_id)+'/responses/'+str(response_id)        
        uri = "%s%s" % (HOST, ENDPOINT)
        #_logger.info(uri)
        
        response = client.get(uri, headers=headers)
        response_json = response.json()
        
        return {
            'status_code': response.status_code,
            'response': response_json
        }
    
    #api
    def get_surveys(self):
        response = {
            'errors': True, 
            'error': "",
            'status_code': "",
            'response': "" 
        }
    
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/surveys"
        
        uri = "%s%s" % (HOST, ENDPOINT)
        
        client_response = client.get(uri, headers=headers)
        client_response_json = client_response.json()
        
        response['status_code'] = client_response.status_code
        if response['status_code']==200:
            response['errors'] = False
            response['response'] = client_response_json
        else:
            if 'error' in client_response_json:
                if 'message' in client_response_json['error']:
                    response['error'] = client_response_json['error']['message']                    
                    self.sack_message_error(response['error'], ENDPOINT)#Slack_message_error
                             
        return response
    
    #api            
    def get_users_me(self):
        response = {
            'errors': True, 
            'error': "",
            'status_code': "",
            'response': "" 
        }
    
        client = requests.session()

        headers = {
            "Authorization": "bearer "+str(self.api_access_token),
            "Content-Type": "application/json"
        }
        
        HOST = "https://api.surveymonkey.net"
        ENDPOINT = "/"+str(self.api_version)+"/users/me"
        
        uri = "%s%s" % (HOST, ENDPOINT)
        
        client_response = client.get(uri, headers=headers)
        client_response_json = client_response.json()
        
        response['status_code'] = client_response.status_code
        if response['status_code']==200:
            response['errors'] = False
            response['response'] = client_response_json
        else:
            if 'error' in client_response_json:
                if 'message' in client_response_json['error']:
                    response['error'] = client_response_json['error']['message']                    
                    self.sack_message_error(response['error'], ENDPOINT)#Slack_message_error
                             
        return response                            
                                                                                                                                                            