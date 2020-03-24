# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from dateutil.relativedelta import relativedelta
from datetime import datetime
import json

import logging
_logger = logging.getLogger(__name__)

import boto3
from botocore.exceptions import ClientError

class OniadTransaction(models.Model):
    _name = 'oniad.transaction'
    _description = 'Oniad Transaction'
    
    account_payment_id = fields.Many2one(
        comodel_name='account.payment',
        string='Pago'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda'
    )
    amount = fields.Monetary(
        string='Importe'
    )
    tax = fields.Monetary(
        string='Tax'
    )
    total = fields.Monetary(
        string='Total'
    )
    date = fields.Date(
        string='Fecha'
    )
    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User'
    )
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        string='Oniad Address'
    )
    type = fields.Selection(
        selection=[
            ('TYPE_CREDIT','Credito'), 
            ('TYPE_COMMISSION','Comision'),
            ('TYPE_SERVICE','Servicio')                          
        ],
        string='Tipo'
    )
    state = fields.Selection(
        selection=[
            ('STATUS_PENDING','Pendiente'), 
            ('STATUS_COMPLETED','Completada'),
            ('STATUS_CANCELLED','Cancelada')                          
        ],
        string='Estado'
    )
    actor = fields.Selection(
        selection=[
            ('ACTOR_ONIAD','Oniad'), 
            ('ACTOR_USER','Usuario'),
            ('ACTOR_AGENCY','Agencia'),
            ('ACTOR_ACCOUNT','Account')                          
        ],
        string='Actor'
    )
    medium = fields.Selection(
        selection=[
            ('MEDIUM_STRIPE','Stripe'), 
            ('MEDIUM_BRAINTREE','Braintree'),
            ('MEDIUM_INTERNAL','Interno'),
            ('MEDIUM_OFFLINE','Offline')                          
        ],
        string='Medium'
    )
    subject = fields.Selection(
        selection=[
            ('SUBJECT_CHARGE','Pago ONiAD'), 
            ('SUBJECT_VOUCHER','Cup�n aplicado'),
            ('SUBJECT_BANNERS','Dise�o de creatividades'),
            ('SUBJECT_COMPENSATION','Compensaci�n comercial'),
            ('SUBJECT_GIFT','Promoci�n'),
            ('SUBJECT_REFUND','Reembolso'),
            ('SUBJECT_CONVERT_COMMISSION_TO_CREDIT','Comisi�n Afiliado a cr�dito'),
            ('SUBJECT_CONVERT_AGENCYCOMMISSION_TO_CREDIT','Comisi�n Partner a cr�dito'),
            ('SUBJECT_SETTLEMENT','Liquidaci�n'),
            ('SUBJECT_TRANSFER','Transferencia'),
            ('SUBJECT_COMMISSION_RECOMMENDED','Programa de recomendados'),
            ('SUBJECT_COMMISSION_AGENCY','Programa de Partners'),
            ('SUBJECT_COMMISSION','Programa de Afiliados')                          
        ],
        string='Asunto'
    )
    
    @api.one
    def check_account_payment(self):
        #define
        stranger_ids_need_skip = [1743, 52076, 52270, 52271, 52281]#Fix transacciones devueltas por stripe 'raras'                
        #need_create_account_payment
        need_create_account_payment = False        
        if self.id>94:#Fix eliminar los de 2017
            if self.id not in stranger_ids_need_skip:
                if self.type!='TYPE_COMMISSION':
                    if self.subject in ['SUBJECT_CHARGE', 'SUBJECT_REFUND']:
                        if self.medium=='MEDIUM_STRIPE':
                            if self.create_date>'2020-01-01':
                                need_create_account_payment = True
        #need_create_account_invoice
        need_create_account_invoice = False
        if self.id>94:#Fix eliminar los de 2017
            if self.id not in stranger_ids_need_skip:
                if self.type!='TYPE_COMMISSION':
                    if self.subject in ['SUBJECT_CHARGE', 'SUBJECT_REFUND']:
                        if self.medium=='MEDIUM_OFFLINE':
                            if self.create_date>'2020-02-12':
                                need_create_account_invoice = True
        #operations need_create_account_payment
        if need_create_account_payment==True:
            if self.account_payment_id.id==0:
                #account.payment                                            
                account_payment_vals = {
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'payment_method_id': 1,
                    'state': 'draft',
                    'currency_id': self.currency_id.id,
                    'partner_id': self.oniad_address_id.partner_id.id,
                    'oniad_user_id': self.oniad_user_id.id,
                    'journal_id': int(self.env['ir.config_parameter'].sudo().get_param('oniad_stripe_journal_id')),
                    'amount': self.total,
                    'payment_date': self.date,
                    'oniad_purchase_price': 0,
                    'communication': dict(self.fields_get(allfields=['subject'])['subject']['selection'])[self.subject],
                    'oniad_transaction_id': self.id,                                                                                                 
                }                     
                #oniad_product_id
                if self.type=='TYPE_CREDIT':
                    account_payment_vals['oniad_product_id'] = int(self.env['ir.config_parameter'].sudo().get_param('oniad_credit_product_id'))                
                elif self.type=='TYPE_SERVICE':
                    account_payment_vals['oniad_product_id'] = int(self.env['ir.config_parameter'].sudo().get_param('oniad_service_product_id'))                            
                #oniad_purchase_price
                if self.type=='TYPE_CREDIT':
                    account_payment_vals['oniad_purchase_price'] = self.total*0.5
                #communication                
                    subjects_with_date = ['SUBJECT_CHARGE', 'SUBJECT_REFUND']
                    if self.subject in subjects_with_date:
                        date_explode = self.date.split('-')
                        account_payment_vals['communication'] += ' '+str(date_explode[2])+'/'+str(date_explode[1])+'/'+str(date_explode[0])           
                #SUBJECT_REFUND            
                if self.subject=='SUBJECT_REFUND':
                    account_payment_vals['payment_type'] = 'outbound'
                    account_payment_vals['oniad_purchase_price'] = 0
                    #fix negative amounts
                    if self.total<0:
                        account_payment_vals['amount'] = self.total*-1
                #create                                                                
                account_payment_obj = self.env['account.payment'].sudo().create(account_payment_vals)
                if account_payment_obj.id>0:
                    self.account_payment_id = account_payment_obj.id
                    if self.account_payment_id.state=='draft': 
                        return_post = self.account_payment_id.post()
            else:
                if self.account_payment_id.state=='draft':
                    self.account_payment_id.post()
        #operations need_create_account_invoice
        if need_create_account_invoice==True:
            #check_if_need_create
            account_invoice_line_ids = self.env['account.invoice.line'].search([('oniad_transaction_id', '=', self.id)])
            if len(account_invoice_line_ids)==0:
                #define
                oniad_account_invoice_journal_id = int(self.env['ir.config_parameter'].sudo().get_param('oniad_account_invoice_journal_id'))
                oniad_product_id = int(self.env['ir.config_parameter'].sudo().get_param('oniad_credit_product_id'))
                product = self.env['product.product'].search([('id','=',oniad_product_id)])
                communication = dict(self.fields_get(allfields=['subject'])['subject']['selection'])[self.subject]
                #creamos una factura con la linea de esta transaccion
                account_invoice_vals = {
                    'partner_id': self.oniad_address_id.partner_id.id,
                    'partner_shipping_id': self.oniad_address_id.partner_id.id,
                    'account_id': self.oniad_address_id.partner_id.property_account_receivable_id.id,
                    'journal_id': oniad_account_invoice_journal_id,#Facturas cliente OniAd
                    'date': self.date,
                    'date_invoice': self.date,
                    'date_due': self.date,
                    'state': 'draft',
                    'comment': ' ',
                    'currency_id': self.currency_id.id,
                    'oniad_address_id': self.oniad_address_id.id,                                         
                }
                #user_id
                if self.oniad_user_id.partner_id.id>0:
                    if self.oniad_user_id.partner_id.user_id.id>0:
                        account_invoice_vals['user_id'] = self.oniad_user_id.partner_id.user_id.id                 
                #create
                account_invoice_obj = self.env['account.invoice'].sudo().create(account_invoice_vals)
                #lines
                account_invoice_line_vals = {
                    'invoice_id': account_invoice_obj.id,
                    'oniad_transaction_id': self.id,
                    'name': communication,
                    'quantity': 1,
                    'price_unit': self.total,
                    'account_id': product.property_account_income_id.id,
                    'purchase_price': self.total*0.5,
                    'currency_id': self.currency_id.id,
                    'product_id': oniad_product_id                      
                }                 
                account_invoice_line_obj = self.env['account.invoice.line'].sudo().create(account_invoice_line_vals)
                account_invoice_line_obj._onchange_product_id()
                account_invoice_line_obj._onchange_account_id()                
                #price
                price_unit = self.total/((account_invoice_line_obj.invoice_line_tax_ids.amount/100)+1)
                account_invoice_line_obj.update({
                    'price_unit': round(price_unit,4),
                    'name': communication,
                    'price_subtotal': price_unit
                })
                account_invoice_obj.compute_taxes()
                #valid
                account_invoice_obj.action_invoice_open()
                #el sns se realizaria cuando la factura se validara (generando el PDF y guardandolo en un bucket de S3 y enviando el SNS correspondiente con toda la informacion)                                     
    
    @api.model
    def create(self, values):
        return_item = super(OniadTransaction, self).create(values)
        #operations
        return_item.check_account_payment()
        #return
        return return_item
    
    @api.one
    def write(self, vals):                        
        return_write = super(OniadTransaction, self).write(vals)
        #operations
        self.check_account_payment()
        #return    
        return return_write            
    
    @api.multi    
    def cron_sqs_oniad_transaction(self, cr=None, uid=False, context=None):
        _logger.info('cron_sqs_oniad_transaction')
        
        sqs_oniad_transaction_url = tools.config.get('sqs_oniad_transaction_url')
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
                QueueUrl=sqs_oniad_transaction_url,
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
                        oniad_transaction_ids = self.env['oniad.transaction'].search([('id', '=', id_item)])
                        if len(oniad_transaction_ids)>0:
                            previously_found = True
                        #params
                        data_oniad_transaction = {
                            'currency_id': 1,
                            'amount': str(message_body['amount']),
                            'tax': str(message_body['tax']),
                            'total': str(message_body['total']),
                            'oniad_user_id': int(message_body['actor_destination_id']),
                            'oniad_address_id': int(message_body['address_id']),
                            'type': str(message_body['type']),
                            'state': str(message_body['status']),
                            'actor': str(message_body['actor_origin']),
                            'medium': str(message_body['medium_type']),
                            'subject': str(message_body['subject']),
                            'date': str(message_body['completed_at']),
                            'create_date': str(message_body['completed_at'])
                        }
                        #fix prevent error oniad_user_id
                        if data_oniad_transaction['oniad_user_id']=='0':
                            del data_oniad_transaction['oniad_user_id']
                            #result
                            result_message['statusCode'] = 500
                            result_message['return_body'] = 'El campo oniad_user_id no puede ser 0'
                        #fields_type_date                                                                            
                        fields_type_date = ['date', 'create_date']
                        for field_type_date in fields_type_date:
                            if field_type_date in data_oniad_transaction:
                                if 'T' in data_oniad_transaction[field_type_date]:
                                    field_item_split = data_oniad_transaction[field_type_date].split('T')                            
                                    field_item_split2 = field_item_split[1].split('+')
                                    field_new = field_item_split[0]+' '+field_item_split2[0]
                                    data_oniad_transaction[field_type_date] = field_new
                        #add_id
                        if previously_found==False:
                            data_oniad_transaction['id'] = int(message_body['id'])
                        #search oniad_user_id (prevent errors)
                        if 'oniad_user_id' in data_oniad_transaction:
                            if data_oniad_transaction['oniad_user_id']>0:
                                oniad_user_ids = self.env['oniad.user'].search([('id', '=', int(data_oniad_transaction['oniad_user_id']))])
                                if len(oniad_user_ids)==0:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = 'No existe el oniad_user_id='+str(data_oniad_transaction['oniad_user_id'])
                        #search oniad_address_id (prevent errors)
                        if 'oniad_address_id' in data_oniad_transaction:
                            if data_oniad_transaction['oniad_address_id']==0:
                                result_message['statusCode'] = 500
                                result_message['return_body'] = 'El campo oniad_address_id no puede ser 0'
                            else:
                                oniad_address_ids = self.env['oniad.address'].search([('id', '=', int(data_oniad_transaction['oniad_address_id']))])
                                if len(oniad_address_ids)==0:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = 'No existe el oniad_address_id='+str(data_oniad_transaction['oniad_address_id'])                                                                                           
                        #final_operations
                        result_message['data'] = data_oniad_transaction
                        _logger.info(result_message)
                        #create-write
                        if result_message['statusCode']==200:#error, data not exists
                            if previously_found==False:
                                oniad_transaction_obj = self.env['oniad.transaction'].sudo().create(data_oniad_transaction)
                            else:
                                oniad_transaction_id = oniad_transaction_ids[0]
                                #write
                                oniad_transaction_id.write(data_oniad_transaction)                                                    
                    #remove_message                
                    if result_message['statusCode']==200:                
                        response_delete_message = sqs.delete_message(
                            QueueUrl=sqs_oniad_transaction_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
            
    @api.multi    
    def cron_action_account_invoices_generate(self, cr=None, uid=False, context=None):
        _logger.info('cron_action_account_invoices_generate')   
        #define
        oniad_stripe_journal_id = int(self.env['ir.config_parameter'].sudo().get_param('oniad_stripe_journal_id'))
        oniad_account_invoice_journal_id = int(self.env['ir.config_parameter'].sudo().get_param('oniad_account_invoice_journal_id'))
        oniad_account_invoice_product = int(self.env['ir.config_parameter'].sudo().get_param('oniad_account_invoice_product'))        
        product = self.env['product.product'].search([('id','=',oniad_account_invoice_product)])
        #dates      
        current_date = datetime.today()        
        start_date = current_date + relativedelta(months=-1, day=1)
        end_date = datetime(start_date.year, start_date.month, 1) + relativedelta(months=1, days=-1)        
        
        date_invoice = end_date
        if end_date.day==31 and end_date.month==12:
            date_invoice = date_invoice + relativedelta(days=-1)        
        #oniad_transaction_ids
        oniad_transaction_ids = self.env['oniad.transaction'].search(
            [
                ('id', '>', 94),#Fix eliminar los de 2017
                ('id', 'not in', (1743, 52076, 52270, 52271, 52281)),#Fix transacciones devueltas por stripe 'raras'
                ('type', '=', 'TYPE_CREDIT'),
                ('state', '=', 'STATUS_COMPLETED'),
                ('actor', '=', 'ACTOR_ONIAD'),
                ('medium', '=', 'MEDIUM_STRIPE'),
                ('subject', 'in', ('SUBJECT_CHARGE', 'SUBJECT_REFUND')),                
                ('account_payment_id', '!=', False),
                ('account_payment_id.journal_id', '=', oniad_stripe_journal_id),
                ('account_payment_id.state', 'in', ('posted', 'sent')),
                ('account_payment_id.payment_type', 'in', ('inbound', 'outbound')),
                ('account_payment_id.payment_date', '<=', end_date.strftime("%Y-%m-%d")),
                ('date', '>=', '2020-01-01')#Fix que quitaremos cuando queramos facturas las negativas 'viejas'
            ]
        )
        if len(oniad_transaction_ids)>0:
            partner_payments = {}
            for oniad_transaction_id in oniad_transaction_ids:
                payment_with_invoice = False 
                for account_invoice in oniad_transaction_id.account_payment_id._get_invoices():
                    payment_with_invoice = True
                    
                if payment_with_invoice==False:
                    if oniad_transaction_id.account_payment_id.partner_id.id not in partner_payments:
                        partner_payments[oniad_transaction_id.account_payment_id.partner_id.id] = []
                    #append
                    partner_payments[oniad_transaction_id.account_payment_id.partner_id.id].append(oniad_transaction_id.account_payment_id)
            #operations            
            _logger.info('Facturas a crear: '+str(len(partner_payments)))            
            if len(partner_payments)>0:
                count = 0                
                #for
                for partner_id, partner_payments_item in partner_payments.items():                    
                    count += 1
                    #types
                    partner_payments_by_type = {'inbound': [],'outbound': []}
                    payment_types_item_amount = {'inbound': 0, 'outbound': 0}
                    #calculate_total and by_type
                    for partner_payment_item in partner_payments_item:
                        #amount
                        payment_types_item_amount[str(partner_payment_item.payment_type)] += partner_payment_item.amount
                        #add_items
                        partner_payments_by_type[str(partner_payment_item.payment_type)].append(partner_payment_item)
                    #operations
                    #inbound
                    if payment_types_item_amount['inbound']>0:
                        #partner_payment_by_type_item_0
                        partner_payment_by_type_item_0 = partner_payments_by_type['inbound'][0]
                        #partner
                        partner = partner_payment_by_type_item_0.partner_id
                        #percent                
                        percent = (float(count)/float(len(partner_payments)))*100
                        percent = "{0:.2f}".format(percent)                                    
                        #account.invoice
                        account_invoice_vals = {
                            'oniad_address_id': partner_payment_by_type_item_0.oniad_transaction_id.oniad_address_id.id,
                            'partner_id': partner.id,
                            'partner_shipping_id': partner.id,
                            'partner_id_oniad': partner.id,
                            'account_id': partner.property_account_receivable_id.id,
                            'journal_id': oniad_account_invoice_journal_id,#Facturas cliente OniAd
                            'date': date_invoice,
                            'date_invoice': date_invoice,
                            'date_due': date_invoice,
                            'state': 'draft',
                            'comment': ' ',
                            'currency_id': partner_payment_by_type_item_0.currency_id.id                                         
                        }
                        #user_id (el del partner_payment_by_type_item_0 > oniad_user_id > partner_id > user_id)
                        if partner_payment_by_type_item_0.oniad_transaction_id.id>0:
                            if partner_payment_by_type_item_0.oniad_transaction_id.oniad_user_id.id>0:
                                if partner_payment_by_type_item_0.oniad_transaction_id.oniad_user_id.partner_id.id>0:
                                    if partner_payment_by_type_item_0.oniad_transaction_id.oniad_user_id.partner_id.user_id.id>0:
                                        account_invoice_vals['user_id'] = partner_payment_by_type_item_0.oniad_transaction_id.oniad_user_id.partner_id.user_id.id
                        #continue
                        _logger.info('Prepararmos para generar al partner_id '+str(account_invoice_vals['partner_id'])+" y al partner_shipping_id "+str(partner.id))            
                        account_invoice_obj = self.env['account.invoice'].sudo().create(account_invoice_vals)
                        _logger.info('Factura '+str(account_invoice_obj.id)+' creada correctamente')                        
                        #oniad_root_complete_data
                        account_invoice_obj.oniad_root_complete_data(product, partner_payments_by_type['inbound'])                                                
                        #logger_percent
                        _logger.info(str(percent)+'% ('+str(count)+'/'+str(len(partner_payments))+')')
                    #outbound
                    if payment_types_item_amount['outbound']>0:
                        #partner_payment_by_type_item_0
                        partner_payment_by_type_item_0 = partner_payments_by_type['outbound'][0]
                        #search out_invoice
                        account_invoice_ids_out_invoice = self.env['account.invoice'].search(
                            [
                                ('type', '=', 'out_invoice'),
                                ('partner_id', '=', partner_payment_by_type_item_0.partner_id.id),
                                ('amount_total', '>=', payment_types_item_amount['outbound'])
                            ], order="date_invoice desc"
                        )
                        if len(account_invoice_ids_out_invoice)>0:
                            account_invoice_id_out_invoice = account_invoice_ids_out_invoice[0]
                            _logger.info('Creamos la negativa respecto a la encontrada '+str(account_invoice_id_out_invoice.id))
                            #percent                
                            percent = (float(count)/float(len(partner_payments)))*100
                            percent = "{0:.2f}".format(percent)                                    
                            #account_invoice_vals
                            account_invoice_vals = {
                                'oniad_address_id': account_invoice_id_out_invoice.oniad_address_id.id,
                                'partner_id': account_invoice_id_out_invoice.partner_id.id,
                                'partner_shipping_id': account_invoice_id_out_invoice.partner_id.id,
                                'partner_id_oniad': account_invoice_id_out_invoice.partner_id.id,
                                'account_id': account_invoice_id_out_invoice.partner_id.property_account_receivable_id.id,
                                'journal_id': account_invoice_id_out_invoice.journal_id.id,
                                'date': date_invoice,
                                'date_invoice': date_invoice,
                                'date_due': date_invoice,
                                'state': 'draft',
                                'type': 'out_refund',
                                'origin': account_invoice_id_out_invoice.number,
                                'name': 'Devolucion',
                                'comment': ' ',
                                'currency_id': account_invoice_id_out_invoice.currency_id.id                                         
                            }
                            #user_id
                            if account_invoice_id_out_invoice.user_id.id>0:
                                account_invoice_vals['user_id'] = account_invoice_id_out_invoice.user_id.id                                            
                            #continue
                            _logger.info('Prepararmos para generar al partner_id '+str(account_invoice_vals['partner_id'])+" y al partner_shipping_id "+str(account_invoice_vals['partner_id']))            
                            account_invoice_obj = self.env['account.invoice'].sudo().create(account_invoice_vals)
                            _logger.info('Factura '+str(account_invoice_obj.id)+' creada correctamente')
                            #oniad_root_complete_data
                            account_invoice_obj.oniad_root_complete_data(product, partner_payments_by_type['outbound'])                            
                            #logger_percent
                            _logger.info(str(percent)+'% ('+str(count)+'/'+str(len(partner_payments))+')')                                
                        else:
                            _logger.info('NO se ha encontrado ninguna factura positiva de importe superior - DEBERIA SER TOTALMENTE IMPOSIBLE')