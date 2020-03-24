# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

import json
import boto3

import logging
_logger = logging.getLogger(__name__)

class DatalakeLog(models.Model):
    _name = 'datalake.log'
    _description = 'Datalake Log'    
    
    def sns_arns_google_analytics_reports(self):
        return [
            'arn:aws:sns:eu-west-1:534422648921:oniad-datalake-1-command-google-analytics-result-beahavior-create',
            'arn:aws:sns:eu-west-1:534422648921:oniad-datalake-1-command-google-analytics-result-campaign-create',
            'arn:aws:sns:eu-west-1:534422648921:oniad-datalake-1-command-google-analytics-result-general-create'
        ]
        
    def google_analytics_reports_profile_ids(self):
        return [85831272, 138471441]
     
    @api.multi    
    def cron_generate_ses_google_analytics_reports_yesterday(self, cr=None, uid=False, context=None):
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')                    
        ses_datalake_test = str(self.env['ir.config_parameter'].sudo().get_param('ses_datalake_test'))                                
        
        current_date = datetime.today()
        sns_date = current_date + relativedelta(days=-1)
        
        sns_client = boto3.client('sns', 
            aws_access_key_id=AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='eu-west-1' 
        )
        
        for sns_arn in self.sns_arns_google_analytics_reports():
            for profile_id in self.google_analytics_reports_profile_ids():                                                            
                #test
                test = False
                if ses_datalake_test==True or ses_datalake_test=='True':
                    test = True                                                    
                #publish
                message = {
                    'test': test,
                    'profile_id': profile_id,
                    'date': sns_date.strftime("%Y-%m-%d")
                }                                                                                 
                response = sns_client.publish(
                    TopicArn=sns_arn,    
                    Message=json.dumps(message)    
                )
                _logger.info(message)
                _logger.info(response)
    
    @api.multi    
    def cron_generate_ses_google_analytics_reports_all_year(self, cr=None, uid=False, context=None):
        end_date = datetime.today()
        start_date = datetime(end_date.year,1, 1)                
        
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')                
        ses_datalake_test = str(self.env['ir.config_parameter'].sudo().get_param('ses_datalake_test'))
        
        sns_client = boto3.client('sns', 
            aws_access_key_id=AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='eu-west-1' 
        )
        
        sns_date = start_date
        
        while sns_date.strftime("%Y-%m-%d")!=end_date.strftime("%Y-%m-%d"):
            sns_date = sns_date + relativedelta(days=1)
                        
            for sns_arn in self.sns_arns_google_analytics_reports():
                for profile_id in self.google_analytics_reports_profile_ids():                                                            
                    #test
                    test = False
                    if ses_datalake_test==True or ses_datalake_test=='True':
                        test = True                                                    
                    #publish
                    message = {
                        'test': test,
                        'profile_id': profile_id,
                        'date': sns_date.strftime("%Y-%m-%d")
                    }                                                                                 
                    response = sns_client.publish(
                        TopicArn=sns_arn,    
                        Message=json.dumps(message)    
                    )
                    _logger.info(message)
                    _logger.info(response)
                                                                                   