# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools
import json
import dateutil.parser

import logging
_logger = logging.getLogger(__name__)

import boto3
from botocore.exceptions import ClientError

class OniadCampaign(models.Model):
    _name = 'oniad.campaign'
    _description = 'Oniad Campaign'
    
    name = fields.Char(
        string='Nombre'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda'
    )
    cpm = fields.Monetary(
        string='Cpm'
    )
    cpm_real = fields.Monetary(
        string='Cpm real'
    )
    type = fields.Selection(
        selection=[
            ('0','Prospeccion'),
            ('1','Video'),
            ('2','Retargeting Web'),
            ('3','Retargeting Email'),                                                                                                        
        ],
        string='Tipo', 
    )
    state = fields.Selection(
        selection=[
            ('0','Imcompleto'),
            ('1','Activo'),
            ('2','Inactivo'),
            ('3','En revision'),
            ('4','Pausada'),
            ('5','Terminada'),                                                                                                        
        ],
        string='Estado', 
    )
    during = fields.Integer(
        string='Duracion (dias)'
    )
    active = fields.Boolean(
        string='Activo'
    )
    pricing = fields.Monetary(
        string='Precio'
    )
    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User'
    )
    cpc_price = fields.Monetary(
        string='Cpc precio'
    )
    frecuency = fields.Integer(
        string='Frecuencia'
    )
    brain_active = fields.Boolean(
        string='Brain activo'
    )
    budget_daily = fields.Monetary(
        string='Presupuesto diario'
    )
    date_start = fields.Datetime(
        string='Fecha inicio'
    )
    date_finish = fields.Datetime(
        string='Fecha fin'
    )
    timezone = fields.Char(
        string='Zona horaria'
    )
    spent = fields.Monetary(
        string='Spent'
    )
    spent_at = fields.Datetime(
        string='Spent At'
    )
    
    @api.model    
    def cron_sqs_oniad_campaign(self):
        _logger.info('cron_sqs_oniad_campaign')
        
        sqs_oniad_campaign_url = tools.config.get('sqs_oniad_campaign_url')
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
                QueueUrl=sqs_oniad_campaign_url,
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
                        oniad_campaign_ids = self.env['oniad.campaign'].search([('id', '=', id_item)])
                        if len(oniad_campaign_ids)>0:
                            previously_found = True
                        #params
                        data_oniad_campaign  = {
                            'currency_id': 1,
                            'name': str(message_body['name'].encode('utf-8')),
                            'cpm_real': str(message_body['cpm_real']),
                            'type': str(message_body['type']),
                            'state': str(message_body['state']),
                            'during': str(message_body['during']),
                            'active': True,
                            'pricing': str(message_body['pricing']),
                            'oniad_user_id': int(message_body['user_id']),
                            'cpc_price': str(message_body['cpc_price']),
                            'frecuency': str(message_body['frecuency']),
                            'brain_active': False,
                            'budget_daily': str(message_body['budget_daily']),
                            'timezone': str(message_body['timezone']),
                        }
                        #brain_active
                        if 'brain_active' in message_body:
                            if message_body['brain_active']==1:
                                message_body['brain_active'] = True
                        #active
                        if 'archive' in message_body:
                            if message_body['archive']==False:
                                message_body['active'] = False
                        #date_start
                        if 'date_start' in message_body:
                            if message_body['date_start']!='':
                                date_start = dateutil.parser.parse(str(message_body['date_start']))
                                date_start = date_start.replace() - date_start.utcoffset()
                                data_oniad_campaign['date_start'] = date_start.strftime("%Y-%m-%d %H:%M:%S")                
                        #date_finish
                        if 'date_finish' in message_body:
                            if message_body['date_finish']!='':
                                date_finish = dateutil.parser.parse(str(message_body['date_finish']))
                                date_finish = date_finish.replace() - date_finish.utcoffset()
                                data_oniad_campaign['date_finish'] = date_finish.strftime("%Y-%m-%d %H:%M:%S")
                        #add_id
                        if previously_found==False:
                            data_oniad_campaign['id'] = int(message_body['id'])
                        #search oniad_user_id (prevent errors)
                        if 'oniad_user_id' in data_oniad_campaign:
                            if data_oniad_campaign['oniad_user_id']>0:
                                oniad_user_ids = self.env['oniad.user'].search([('id', '=', int(data_oniad_campaign['oniad_user_id']))])
                                if len(oniad_user_ids)==0:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = 'No existe el campo oniad_user_id='+str(data_oniad_campaign['oniad_user_id'])                            
                        #final_operations
                        result_message['data'] = data_oniad_campaign
                        _logger.info(result_message)
                        #create-write
                        if result_message['statusCode']==200:#error, data not exists
                            if previously_found==False:                            
                                oniad_campaign_obj = self.env['oniad.campaign'].sudo().create(data_oniad_campaign)
                            else:
                                oniad_campaign_id = oniad_campaign_ids[0]
                                #write
                                oniad_campaign_id.write(data_oniad_campaign)                                                    
                    #remove_message                
                    if result_message['statusCode']==200:                
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_oniad_campaign_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
    
    @api.model    
    def cron_sqs_oniad_campaign_report(self):
        _logger.info('cron_sqs_oniad_campaign_report')
        
        sqs_oniad_campaign_report_url = tools.config.get('sqs_oniad_campaign_report_url')
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
                QueueUrl=sqs_oniad_campaign_report_url,
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
                    fields_need_check = ['campaign_id', 'spent', 'spent_at']
                    for field_need_check in fields_need_check:
                        if field_need_check not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'No existe el campo '+str(field_need_check)
                    #operations
                    if result_message['statusCode']==200:
                        campaign_id = int(message_body['campaign_id'])
                        oniad_campaign_ids = self.env['oniad.campaign'].search([('id', '=', campaign_id)])
                        if len(oniad_campaign_ids)==0:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'No se ha encontrado el oniad_campaign_id='+str(campaign_id)
                        else:
                            oniad_campaign_id = oniad_campaign_ids[0]
                            oniad_campaign_id.spent = message_body['spent']
                            #spent_at
                            spent_at = dateutil.parser.parse(str(message_body['spent_at']))
                            spent_at = spent_at.replace() - spent_at.utcoffset()
                            oniad_campaign_id.spent_at = spent_at.strftime("%Y-%m-%d %H:%M:%S")                            
                    #final_operations
                    _logger.info(result_message)
                    #remove_message                
                    if result_message['statusCode']==200:                
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_oniad_campaign_report_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )                                                                                                                 