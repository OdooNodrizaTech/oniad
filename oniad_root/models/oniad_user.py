# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import dateutil.parser
import json

import logging
_logger = logging.getLogger(__name__)

import boto3
from botocore.exceptions import ClientError

class OniadUser(models.Model):
    _name = 'oniad.user'
    _description = 'Oniad User'
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda'
    )
    lang = fields.Char(
        string='Idioma'
    )
    name = fields.Char(
        string='Nombre'
    )
    last_name = fields.Char(
        string='Apellidos'
    )
    uuid = fields.Char(
        string='Uuid'
    )
    email = fields.Char(
        string='Email'
    )
    phone = fields.Char(
        string='Telefono'
    )    
    iso_code = fields.Char(
        string='Iso Code'
    )
    timezone = fields.Char(
        string='Timezone'
    )
    confirmed = fields.Boolean(
        string='Confirmado'
    )
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        string='Direccion'
    )
    oniad_accountmanager_id = fields.Many2one(
        comodel_name='oniad.accountmanager',
        string='Account Manager'
    )
    parent_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Padre'
    )
    type = fields.Selection(
        selection=[
            ('user','Usuario'),
            ('agency','Agencia'),
            ('client_own','Cuenta creada'),                                                                                                                
        ],
        string='Tipo', 
    )
    oniad_managed = fields.Boolean(
        string='Oniad Managed'
    )
    spent_cost = fields.Monetary(
        string='Spent Cost'
    )        
    spent_min_date = fields.Date(
        string='Spent Min Date'
    )
    spent_max_date = fields.Date(
        string='Spent Max Date'
    )    
    last_login = fields.Datetime(
        string='Last Login'
    )
    odoo_lead = fields.Char(
        string='Odoo Lead'
    )
    welcome_lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Welcome Lead Id'
    )
    tag_ids = fields.One2many('oniad.user.tag', 'oniad_user_id', string='Tags')
    
    oniad_user_id_link = fields.Char(
        compute='_oniad_user_id_link',
        string='OniAd User',
        store=False
    )            
    
    @api.multi        
    def _oniad_user_id_link(self):
        for record in self:
            if record.id>0: 
                record.oniad_user_id_link = 'https://platform.oniad.com/backend/admin/supadmin/card/'+str(record.id)
        
    @api.one
    def check_res_partner(self):
        partner_vals = {
            'name': str(self.name.encode('utf-8')),
            'customer': True,
            'email': self.email,             
            'lang': str(self.lang)
        }
        #lastname
        if self.last_name!=False:
            partner_vals['name'] = str(self.name.encode('utf-8'))+' '+str(self.last_name.encode('utf-8'))
        #phone
        if self.phone!=False:
            first_char_phone = self.phone[:1]
            mobile_first_chars = [6,7]
            if first_char_phone in mobile_first_chars:
                partner_vals['mobile'] = self.phone
            else:
                partner_vals['phone'] = self.phone            
        #oniad_accountmanager_id
        if self.oniad_accountmanager_id.user_id.id>0:
            partner_vals['user_id'] = self.oniad_accountmanager_id.user_id.id        
        #operations
        if self.partner_id.id==0:
            need_create_partner = True
            #convert lead to opportunity
            if self.odoo_lead!=False and self.odoo_lead!='':
                need_create_partner = False
                #search
                crm_lead_ids = self.env['crm.lead'].search([('register_token', '=', self.odoo_lead)])
                if len(crm_lead_ids)>0:
                    for crm_lead_id in crm_lead_ids:
                        if crm_lead_id.type=='lead':
                            #convert_opportunity_create_partner
                            crm_lead_id.convert_opportunity_create_partner(False, False)
                            #need_update?
                            if crm_lead_id.partner_id.id>0:
                                self.partner_id = crm_lead_id.partner_id.id                                
                            else:
                                need_create_partner = True                      
            #create
            if need_create_partner==True:
                res_partner_obj = self.env['res.partner'].sudo().create(partner_vals)
                if res_partner_obj.id>0:
                    self.partner_id = res_partner_obj.id                    
        else:
            self.partner_id.update(partner_vals)    
    
    @api.one
    def check_welcome_lead(self):
        if self.welcome_lead_id.id==0:
            if self.type in ['user', 'agency']:
                if self.partner_id.id>0:
                    if self.partner_id.user_id.id>0:
                        if self.create_date>='2020-02-12':
                            #define
                            current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                            #need_check
                            need_check = False
                            if self.phone!=False:
                                need_check = True
                            else:
                                diff = datetime.strptime(str(current_date.strftime("%Y-%m-%d %H:%M:%S")), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(self.create_date), '%Y-%m-%d %H:%M:%S')
                                dateTimeDifferenceInHours = diff.total_seconds() / 3600
                                if dateTimeDifferenceInHours>=2:
                                    need_check = True

                            if need_check==True:
                                crm_lead_ids = self.env['crm.lead'].search(
                                    [
                                        ('partner_id', '=', self.partner_id.id),
                                        ('lead_oniad_type', '=', 'welcome'),
                                        ('type', '=', 'opportunity'),
                                        ('commercial_activity_type', '=', 'account')
                                    ]
                                )
                                if len(crm_lead_ids)>0:
                                    for crm_lead_id in crm_lead_ids:
                                        self.welcome_lead_id = crm_lead_id.id
                                else:
                                    oniad_welcome_lead_template_id = int(self.env['ir.config_parameter'].sudo().get_param('oniad_welcome_lead_template_id'))
                                    #es necesario crear lead
                                    crm_lead_vals = {
                                        'partner_id': self.partner_id.id,
                                        'lead_oniad_type': 'welcome',
                                        'type': 'opportunity',
                                        'commercial_activity_type': 'account',
                                        'active': True,
                                        'probability': 10,
                                        'team_id': 1,#Equipo de ventas por defecto
                                        'stage_id': 1,#Sin contactar
                                        'name': 'Hola, quiero ayudarte a mejorar tus campañas',
                                        'description': 'Presentarse y ayudar a nuevos clientes',
                                        'color': 5
                                    }
                                    #phone
                                    if self.phone!=False:
                                        crm_lead_vals['phone'] = str(self.phone)
                                    #user_id
                                    if self.oniad_accountmanager_id.id>0:
                                        if self.oniad_accountmanager_id.user_id.id>0:
                                            crm_lead_vals['user_id'] = self.oniad_accountmanager_id.user_id.id
                                    #create
                                    if 'user_id' in crm_lead_vals:
                                        crm_lead_obj = self.env['crm.lead'].sudo(crm_lead_vals['user_id']).create(crm_lead_vals)#Fix create simullate user_id
                                    else:
                                        crm_lead_obj = self.env['crm.lead'].sudo().create(crm_lead_vals)
                                    #si corresponde enviamos un email
                                    if 'phone' not in crm_lead_vals:
                                        #enviamos_email
                                        crm_lead_obj.action_send_mail_with_template_id(oniad_welcome_lead_template_id)#Plantilla Iniciativa/Oportunidad: BIENVENIDO/A A ONiAd (id=54)
                                        #update
                                        crm_lead_obj.stage_id=2#Ayuda ofrecida
                                        next_activity_id_date_action = current_date + relativedelta(days=7)
                                        crm_lead_obj.title_action = 'Revisar contacto usuario'
                                        crm_lead_obj.next_activity_id = 3#Tarea
                                        crm_lead_obj.date_action = next_activity_id_date_action
                                    #update
                                    self.welcome_lead_id = crm_lead_obj.id
    
    @api.one
    def check_sleep_lead(self):
        if self.create_date>='2020-01-12':
            if self.tag_ids!=False:
                user_dormido = False
                if len(self.tag_ids)>0:
                    for tag_id in self.tag_ids:
                        if tag_id.tag=='ESTADO_DORMIDO':
                            user_dormido = True                    
                #user_dormido
                if user_dormido==True:
                    crm_lead_ids = self.env['crm.lead'].search(
                        [
                            ('partner_id', '=', self.partner_id.id),
                            ('lead_oniad_type', '=', 'sleep'),
                            ('type', '=', 'opportunity'),
                            ('commercial_activity_type', '=', 'account'),
                            ('active', '=', True),
                            ('probability', '>', 0),
                            ('probability', '<', 100)                  
                        ]
                    )
                    if len(crm_lead_ids)==0:
                        #crm_lead_vals
                        crm_lead_vals = {
                            'partner_id': self.partner_id.id,
                            'lead_oniad_type': 'sleep',
                            'type': 'opportunity',
                            'commercial_activity_type': 'account',
                            'active': True,
                            'probability': 10,
                            'team_id': 1,#Equipo de ventas por defecto
                            'stage_id': 1,#Sin contactar
                            'name': 'Cliente dormid',
                            'description': 'Despertar al cliente',
                            'color': 5
                        }
                        #phone
                        if self.phone!=False:
                            crm_lead_vals['phone'] = str(self.phone) 
                        #user_id
                        if self.oniad_accountmanager_id.id>0:
                            if self.oniad_accountmanager_id.user_id.id>0:
                                crm_lead_vals['user_id'] = self.oniad_accountmanager_id.user_id.id
                        #create
                        if 'user_id' in crm_lead_vals:
                            crm_lead_obj = self.env['crm.lead'].sudo(crm_lead_vals['user_id']).create(crm_lead_vals)#Fix create simullate user_id
                        else:                                                
                            crm_lead_obj = self.env['crm.lead'].sudo().create(crm_lead_vals)                        
    
    @api.model
    def create(self, values):
        return_item = super(OniadUser, self).create(values)
        #operations
        return_item.check_res_partner()
        return_item.check_welcome_lead()
        #return
        return return_item
    
    @api.one
    def write(self, vals):
        #user_id_old
        user_id_old = 0
        if self.partner_id.id>0:
            if self.partner_id.user_id.id>0:
                user_id_old = self.partner_id.user_id.id
        #write 
        return_write = super(OniadUser, self).write(vals)                        
        #operations
        self.check_res_partner()
        self.check_welcome_lead()
        self.check_sleep_lead()
        #user_id_new
        user_id_new = 0
        if self.partner_id.id>0:
            if self.partner_id.user_id.id>0:
                user_id_new = self.partner_id.user_id.id
        #reasign_crm_leads
        if user_id_new>0:
            if user_id_old!=user_id_new:
                self.reasign_crm_leads()
        #return
        return return_write
            
    @api.one
    def reasign_crm_leads(self):
        if self.partner_id.id>0:
            if self.partner_id.user_id.id>0:
                crm_lead_ids = self.env['crm.lead'].search(
                    [
                        ('partner_id', '=', self.partner_id.id),
                        ('type', '=', 'opportunity'),
                        ('active', '=', True),
                        ('probability', '>', 0),
                        ('probability', '<', 100)                  
                    ]
                )
                if len(crm_lead_ids)>0:
                    for crm_lead_id in crm_lead_ids:
                        crm_lead_id.user_id = self.partner_id.user_id.id
                        #mail_followers (remove all) > fix remove aditional res.user incorrect
                        mail_followers_ids = self.env['mail.followers'].search(
                            [
                                ('res_model', '=', 'crm.lead'), 
                                ('res_id', '=', crm_lead_id.id)
                            ]
                        )
                        if len(mail_followers_ids)>0:
                            for mail_followers_id in mail_followers_ids:
                                if mail_followers_id.partner_id.id != crm_lead_id.partner_id.id:
                                    mail_followers_id.unlink()
                        #add_new (user_id)
                        mail_followers_vals = {
                            'res_model': 'crm.lead',
                            'res_id': crm_lead_id.id,
                            'partner_id': crm_lead_id.user_id.partner_id.id,
                            'subtype_ids': [(4, [1])]
                        }
                        mail_followers_obj = self.env['mail.followers'].sudo().create(mail_followers_vals)                                    
    
    @api.multi    
    def cron_sqs_oniad_user(self, cr=None, uid=False, context=None):
        _logger.info('cron_sqs_oniad_user')
        
        sqs_oniad_user_url = tools.config.get('sqs_oniad_user_url')
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
                QueueUrl=sqs_oniad_user_url,
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
                        oniad_user_ids = self.env['oniad.user'].search([('id', '=', id_item)])
                        if len(oniad_user_ids)>0:
                            previously_found = True                        
                        #params
                        data_oniad_user = {
                            'currency_id': 1,
                            'lang': str(message_body['lang']),
                            'uuid': str(message_body['uuid']),
                            'email': str(message_body['email']),
                            'iso_code': str(message_body['iso_code']),
                            'confirmed': str(message_body['confirmed']),
                            'type': 'user',
                            'oniad_managed': str(message_body['oniad_managed'])
                        }
                        #name
                        try:
                            data_oniad_user['name'] = str(message_body['name'].encode('utf-8'))
                        except:
                            data_oniad_user['name'] = str(message_body['name'])
                        #created_at
                        if 'created_at' in message_body:
                            if message_body['created_at']!=None:
                                created_at = dateutil.parser.parse(str(message_body['created_at']))
                                created_at = created_at.replace() - created_at.utcoffset()
                                data_oniad_user['create_date'] = created_at.strftime("%Y-%m-%d %H:%M:%S")
                        #last_login
                        if 'last_login' in message_body:
                            if message_body['last_login']!=None:
                                if message_body['last_login']!='':
                                    last_login = dateutil.parser.parse(str(message_body['last_login']))
                                    last_login = last_login.replace() - last_login.utcoffset()
                                    data_oniad_user['last_login'] = last_login.strftime("%Y-%m-%d %H:%M:%S")
                        #fields_need_check
                        fields_need_check = ['last_name', 'phone', 'timezone', 'parent_id', 'confirmed']
                        for field_need_check in fields_need_check:
                            if field_need_check in message_body:
                                if message_body[field_need_check]!='':
                                    if message_body[field_need_check]!=None:
                                        if field_need_check in ['last_name']:
                                            try:
                                                data_oniad_user[field_need_check] = str(message_body[field_need_check].encode('utf-8'))
                                            except:
                                                data_oniad_user[field_need_check] = str(message_body[field_need_check])
                                        else:
                                            data_oniad_user[field_need_check] = str(message_body[field_need_check])
                        #parent_id
                        if 'parent_id' in data_oniad_user:
                            if data_oniad_user['parent_id']=='0':
                                del data_oniad_user['parent_id']
                        #address_id
                        if 'address_id' in message_body:
                            if message_body['address_id']!='':
                                if message_body['address_id']!=None:
                                    if int(message_body['address_id'])!=0:
                                        data_oniad_user['oniad_address_id'] = int(message_body['address_id'])        
                        #accountmanager_id
                        if 'accountmanager_id' in message_body:
                            if message_body['accountmanager_id']!='':
                                if message_body['accountmanager_id']!=None:
                                    if int(message_body['accountmanager_id'])!=0:
                                        data_oniad_user['oniad_accountmanager_id'] = int(message_body['accountmanager_id'])        
                        #type
                        if 'roles' in message_body:
                            #ROLE_CLIENT_OWN
                            if 'ROLE_CLIENT_OWN' in message_body['roles']:
                                data_oniad_user['type'] = 'client_own'
                            #ROLE_AGENCY
                            if 'ROLE_AGENCY' in message_body['roles']:
                                data_oniad_user['type'] = 'agency'                
                        #spent
                        if 'spent' in message_body:
                            if message_body['spent']!=None:
                                #cost
                                if message_body['spent']['cost']!=None:
                                    data_oniad_user['spent_cost'] = message_body['spent']['cost']
                                #min_date
                                if message_body['spent']['min_date']!=None:
                                    data_oniad_user['spent_min_date'] = message_body['spent']['min_date']
                                #max_date
                                if message_body['spent']['max_date']!=None:
                                    data_oniad_user['spent_max_date'] = message_body['spent']['max_date']
                        #boolean_fields
                        boolean_fields = ['confirmed', 'oniad_managed']
                        for boolean_field in boolean_fields:
                            if boolean_field in data_oniad_user:
                                if data_oniad_user[boolean_field]=='True':
                                    data_oniad_user[boolean_field] = True
                                elif data_oniad_user[boolean_field]=='False':
                                    data_oniad_user[boolean_field] = False
                                else:
                                    data_oniad_user[boolean_field]
                        #odoo_lead
                        if 'context' in message_body:
                            if message_body['context']!='':
                                if message_body['context']!=None:
                                    if 'odoo_lead' in message_body['context']:
                                        if message_body['context']['odoo_lead']!='':                    
                                            if message_body['context']['odoo_lead']!=None:
                                                data_oniad_user['odoo_lead'] = str(message_body['context']['odoo_lead'])                        
                        #add_id
                        if previously_found==False:
                            data_oniad_user['id'] = int(message_body['id'])
                        #search oniad_address_id (prevent errors)
                        if 'oniad_address_id' in data_oniad_user:
                            if data_oniad_user['oniad_address_id']>0:
                                oniad_address_ids = self.env['oniad.address'].search([('id', '=', int(data_oniad_user['oniad_address_id']))])
                                if len(oniad_address_ids)==0:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = 'No existe la direccion '+str(data_oniad_user['oniad_address_id'])
                        #final_operations
                        result_message['data'] = data_oniad_user
                        _logger.info(result_message)
                        #create-write
                        if result_message['statusCode']==200:#error, data not exists
                            if previously_found==False:                            
                                oniad_user_obj = self.env['oniad.user'].sudo().create(data_oniad_user)
                            else:
                                oniad_user_id = oniad_user_ids[0]
                                #write
                                oniad_user_id.write(data_oniad_user)                                                           
                    #remove_message
                    if result_message['statusCode']==200:                
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_oniad_user_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
            
    @api.multi    
    def cron_sqs_oniad_usertag(self, cr=None, uid=False, context=None):
        _logger.info('cron_sqs_oniad_usertag')
        
        sqs_oniad_usertag_url = tools.config.get('sqs_oniad_usertag_url')
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
                QueueUrl=sqs_oniad_usertag_url,
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
                    #general
                    #fields_need_check
                    fields_need_check = ['id', 'tags']
                    for field_need_check in fields_need_check:
                        if field_need_check not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'No existe el campo '+str(field_need_check)
                    #operations
                    if result_message['statusCode']==200:
                        item_id = int(message_body['id'])
                        oniad_user_ids = self.env['oniad.user'].search([('id', '=', item_id)])
                        if len(oniad_user_ids)==0:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'No se encuentra el user_id='+str(item_id)
                        else:
                            oniad_user_id = oniad_user_ids[0]
                            #tag_ids
                            if len(message_body['tags'])>0:
                                tag_ids = []
                                for tag in message_body['tags']:
                                    tag_ids.append({                                                                
                                        'tag': str(tag)
                                    })
                                #update  
                                result_message['tag_ids'] = tag_ids                                                 
                                oniad_user_id.tag_ids = tag_ids
                    #final_operations
                    _logger.info(result_message)                                
                    #remove_message
                    if result_message['statusCode']==200:                
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_oniad_usertag_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )        
        
    @api.one
    def action_send_mail_with_template_id(self, template_id=False):
        if template_id!=False:                                        
            mail_template_item = self.env['mail.template'].search([('id', '=', template_id)])[0]                                
            mail_compose_message_vals = {                    
                'author_id': 1,
                'record_name': self.name,                                                                                                                                                                                           
            }
            #Fix user_id
            if self.user_id.id>0:
                mail_compose_message_vals['author_id'] = self.user_id.partner_id.id
                
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo(self.user_id.id).create(mail_compose_message_vals)
            else:            
                mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(mail_compose_message_vals)
                
            return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_item.id, 'comment', 'crm.lead', self.id)                                
            
            mail_compose_message_obj.update({
                'author_id': mail_compose_message_vals['author_id'],
                'template_id': mail_template_item.id,
                'composition_mode': 'comment',
                'model': 'crm.lead',
                'res_id': self.id,
                'body': return_onchange_template_id['value']['body'],
                'subject': return_onchange_template_id['value']['subject'],
                'email_from': return_onchange_template_id['value']['email_from'],
                'partner_ids': return_onchange_template_id['value']['partner_ids'],
                #'attachment_ids': return_onchange_template_id['value']['attachment_ids'],
                'record_name': mail_compose_message_vals['record_name'],
                'no_auto_thread': False,                     
            })                                         
            mail_compose_message_obj.send_mail_action()                                                                                                                
            return True             