# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields, tools
from openerp.exceptions import Warning
import uuid

import boto3, json
from botocore.exceptions import ClientError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
            
    margin = fields.Monetary(         
        string='Margen'
    )
    #override date
    date = fields.Date(
        string='Fecha contable',
        copy=False,
        help="Dejar vacio para usar la fecha de factura",
        track_visibility='always',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    uuid = fields.Char(
        string='Uuid'
    )
        
    @api.model
    def create(self, values):
        return_object = super(AccountInvoice, self).create(values)
        return_object.uuid = uuid.uuid4()
        return return_object        
    
    @api.multi    
    def cron_account_invoice_uuid_generate(self, cr=None, uid=False, context=None):
        account_invoice_ids = self.env['account.invoice'].search([('uuid', '=', False)])
        if len(account_invoice_ids)>0:
            for account_invoice_id in account_invoice_ids:
                account_invoice_id.uuid = uuid.uuid4()
    
    @api.multi    
    def cron_account_invoice_send_sns_custom(self, cr=None, uid=False, context=None):
        account_invoice_ids = self.env['account.invoice'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('open', 'paid')),
                ('type', 'in', ('out_invoice', 'out_refund')),
                ('date_invoice', '>=', '2020-01-01')
            ]
        )
        if len(account_invoice_ids)>0:
            _logger.info('Total='+str(len(account_invoice_ids)))
            for account_invoice_id in account_invoice_ids:
                _logger.info('Enviando SNS '+str(account_invoice_id.id))
                account_invoice_id.action_send_sns(False)
    
    @api.multi    
    def cron_account_invoice_upload_to_s3_generate(self, cr=None, uid=False, context=None):
        account_invoice_ids = self.env['account.invoice'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('open', 'paid')),
                ('type', 'in', ('out_invoice', 'out_refund'))
            ]
        )
        if len(account_invoice_ids)>0:
            _logger.info(len(account_invoice_ids))            
            for account_invoice_id in account_invoice_ids:
                _logger.info('Generando factura '+str(account_invoice_id.id))
                #account_invoice_id.action_upload_pdf_to_s3()
                account_invoice_id.action_send_sns(False)
                    
    @api.one
    def action_upload_pdf_to_s3(self):
        if self.state in ['open', 'paid']:
            if self.type in ['out_invoice', 'out_refund']:
                #define
                AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
                AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
                AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
                s3_bucket_docs_oniad_com = tools.config.get('s3_bucket_docs_oniad_com')        
                #boto3
                s3 = boto3.client(
                    's3',
                    region_name=AWS_SMS_REGION_NAME, 
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key= AWS_SECRET_ACCESS_KEY
                )
                #get_pdf
                report_invoice_pdf_content = self.env['report'].get_pdf([self.id], 'account.report_invoice')
                #put_object        
                response_put_object = s3.put_object(Body=report_invoice_pdf_content, Bucket=s3_bucket_docs_oniad_com, Key='account-invoice/'+str(self.uuid)+'.pdf')

    @api.multi
    def action_send_sns_multi(self):
        for item in self:
            _logger.info('Enviando SNS ' + str(item.id))
            item.action_send_sns(False)

    @api.one
    def action_send_sns(self, regenerate_pdf=True):
        if self.state in ['open', 'paid']:
            if self.type in ['out_invoice', 'out_refund']:
                action_response = True
                #action_upload_pdf_to_s3
                if regenerate_pdf==True:
                    self.action_upload_pdf_to_s3()
                #define
                ses_sqs_url = tools.config.get('ses_sqs_url')
                AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
                AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
                AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
                s3_bucket_docs_oniad_com = tools.config.get('s3_bucket_docs_oniad_com')                        
                #boto3
                sns = boto3.client(
                    'sns',
                    region_name=AWS_SMS_REGION_NAME, 
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key= AWS_SECRET_ACCESS_KEY
                )        
                #message        
                message = {
                    'id': int(self.id),
                    'uuid': str(self.uuid),
                    'number': str(self.number),
                    'currency': str(self.currency_id.name),
                    'oniad_address_id': int(self.oniad_address_id.id),
                    'payment_mode_id': {
                        'id': int(self.payment_mode_id.id),
                        'name': str(self.payment_mode_id.name)
                    },
                    'payment_term_id': {
                        'id': int(self.payment_term_id.id),
                        'name': str(self.payment_term_id.name)
                    },
                    'state': str(self.state),
                    'create_date': str(self.create_date),
                    'date_invoice': str(self.date_invoice),
                    'date_due': str(self.date_due),
                    'invoice_with_risk': self.invoice_with_risk,            
                    'type': str(self.type),
                    'amount_untaxed': self.amount_untaxed,
                    'amount_tax': self.amount_tax,
                    'amount_total': self.amount_total,
                    'residual': self.residual,
                    'partner_credit_limit': self.partner_id.credit_limit,
                    'partner_max_credit_limit_allow': self.partner_id.max_credit_limit_allow,
                    'url_pdf': 'https://docs.oniad.com/account-invoice/'+str(self.uuid)+'.pdf',
                    's3_pdf': str(s3_bucket_docs_oniad_com)+'/account-invoice/'+str(self.uuid)+'.pdf',
                    'invoice_line_ids': [],
                    'tax_line_ids': [],
                    'payment_ids': []
                }
                #invoice_line_ids
                if len(self.invoice_line_ids)>0:
                    for invoice_line_id in self.invoice_line_ids:
                        message_invoice_line_id = {
                            'name': str(invoice_line_id.name.encode('utf-8')),
                            'quantity': invoice_line_id.quantity,
                            'price_unit': invoice_line_id.price_unit,
                            'price_subtotal': invoice_line_id.price_unit,
                            'discount': invoice_line_id.price_unit,
                            'oniad_transaction_id': int(invoice_line_id.oniad_transaction_id.id)
                        }
                        message['invoice_line_ids'].append(message_invoice_line_id)
                #tax_line_ids
                if len(self.tax_line_ids)>0:
                    for tax_line_id in self.tax_line_ids:
                        message_tax_line_id = {
                            'name': str(tax_line_id.name.encode('utf-8')),
                            'base': tax_line_id.base,
                            'amount': tax_line_id.amount,
                        }
                        message['tax_line_ids'].append(message_tax_line_id)
                #payment_ids
                if len(self.payment_ids)>0:
                    for payment_id in self.payment_ids:
                        message_payment_id = {
                            'id': int(payment_id.id),
                            'communication': str(payment_id.communication.encode('utf-8')),
                            'payment_date': str(payment_id.payment_date),
                            'amount': payment_id.amount,
                            'oniad_transaction_id': int(payment_id.oniad_transaction_id.id)
                        }
                        message['payment_ids'].append(message_payment_id)
                #enviroment
                enviroment = 'dev'
                web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                if '//erp.oniad.com' in web_base_url:
                    enviroment = 'prod'                    
                #sns_name            
                sns_name = 'oniad-platform-command-odoo-account-invoice'
                if enviroment=='dev':
                    sns_name = 'oniad-platform_dev-command-odoo-account-invoice'
                #publish
                response = sns.publish(
                    TopicArn='arn:aws:sns:eu-west-1:534422648921:'+str(sns_name),
                    Message=json.dumps(message, indent=2),
                    MessageAttributes={
                        'Headers': {
                            'DataType': 'String',
                            'StringValue': json.dumps([{'type': 'Oniad\\Domain\\Odoo\\OdooInvoiceAvailableEvent'},[]])
                        }
                    }                                
                )
                #logger
                _logger.info({
                    'enviroment': enviroment,
                    'sns_name': sns_name
                })
                #check
                if 'MessageId' not in response:
                    action_response = False
                else:
                    _logger.info(sns_name)                           
                #return
                return action_response
    
    @api.one
    def action_calculate_margin(self):
        if self.id>0:
            if self.invoice_line_ids!=False:
                margin_total = 0            
                for invoice_line_id in self.invoice_line_ids:
                    margin_total = margin_total + invoice_line_id.purchase_price
            
                self.margin = margin_total
    
    @api.one
    def write(self, vals):      
        #super                                                               
        return_object = super(AccountInvoice, self).write(vals)
        #check_if_paid
        if vals.get('state')=='paid':
            #action_send_sns
            self.action_send_sns(True)
        #return
        return return_object
    
    @api.multi
    def action_invoice_open(self):
        if self.partner_id.vat==False:
            raise Warning("Es necesario definir un CIF/NIF para el cliente de la factura.\n")
        elif self.type=="in_invoice" and self.reference==False:
            raise Warning("Es necesario definir una referencia de proveedor para validar la factura de compra.\n")            
        else:
            return_object = super(AccountInvoice, self).action_invoice_open()
            for account_invoice_item in self:            
                account_invoice_item.action_calculate_margin()#Fix calculate margin            
            #action_send_sns
            account_invoice_item.action_send_sns(True)
            #return                            
            return return_object        
                    
    @api.one    
    def action_auto_create_message_slack(self):
        return False                    