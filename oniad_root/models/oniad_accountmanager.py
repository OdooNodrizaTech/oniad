# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import json

import logging
_logger = logging.getLogger(__name__)

import boto3
from botocore.exceptions import ClientError

class OniadAccountmanager(models.Model):
    _name = 'oniad.accountmanager'
    _description = 'Oniad Accountmanager'
    
    name = fields.Char(        
        compute='_get_name',
        string='Nombre',
        store=False
    )
    
    @api.one        
    def _get_name(self):            
        for obj in self:
            obj.name = obj.email
            
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario'
    )
    email = fields.Char(
        string='Email'
    )
    
    @api.model    
    def cron_sqs_oniad_accountmanager(self):
        _logger.info('cron_sqs_oniad_accountmanager')
        
        sqs_oniad_accountmanager_url = tools.config.get('sqs_oniad_accountmanager_url')
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')                        
        #boto3
        sqs = boto3.client(
            'sqs',
            region_name=AWS_SMS_REGION_NAME, 
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key= AWS_SECRET_ACCESS_KEY
        )        
        # Receive message from SQS queue
        total_messages = 10
        while total_messages>0:
            response = sqs.receive_message(
                QueueUrl=sqs_oniad_accountmanager_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )
            if 'Messages' in response:
                total_messages = len(response['Messages'])
            else:
                total_messages = 0
            #continue
            if 'Messages' in response:
                for message in response['Messages']:
                    #message_body           
                    message_body = json.loads(message['Body'])
                    #fix message
                    if 'Message' in message_body:
                        message_body = json.loads(message_body['Message'])
                    #result_message
                    result_message = {
                        'statusCode': 200,
                        'return_body': 'OK',
                        'message': message_body
                    }
                    #fields_need_check
                    fields_need_check = ['id']
                    for field_need_check in fields_need_check:
                        if field_need_check not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'No existe el campo '+str(field_need_check)
                    #operations
                    if result_message['statusCode']==200:
                        previously_found = False
                        id_item = int(message_body['id'])
                        oniad_accountmanager_ids = self.env['oniad.accountmanager'].search([('id', '=', id_item)])
                        if len(oniad_accountmanager_ids)>0:
                            previously_found = True
                        #params
                        data_oniad_accountmanager = {
                            'email': str(message_body['email'])
                        }
                        #add_id
                        if previously_found==False:
                            data_oniad_accountmanager['id'] = int(message_body['id'])                                            
                        #final_operations
                        _logger.info(data_oniad_accountmanager)
                        #create-write
                        if previously_found==False:                            
                            oniad_accountmanager_obj = self.env['oniad.accountmanager'].sudo().create(data_oniad_accountmanager)
                        else:
                            oniad_accountmanager_id = oniad_accountmanager_ids[0]
                            #write
                            oniad_accountmanager_id.write(data_oniad_accountmanager)                                                    
                    #final_operations
                    result_message['data'] = data_oniad_accountmanager
                    _logger.info(result_message)
                    #remove_message                
                    if result_message['statusCode']==200:                
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_oniad_accountmanager_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )                