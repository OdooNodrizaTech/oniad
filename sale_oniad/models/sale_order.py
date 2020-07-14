# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields, tools
from openerp.exceptions import Warning
import uuid

import boto3, json
from botocore.exceptions import ClientError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
                
    uuid = fields.Char(
        string='Uuid'
    )
        
    @api.model
    def create(self, values):
        return_object = super(SaleOrder, self).create(values)
        return_object.uuid = uuid.uuid4()
        return return_object        
    
    @api.multi    
    def cron_sale_order_uuid_generate(self, cr=None, uid=False, context=None):
        sale_order_ids = self.env['sale.order'].search([('uuid', '=', False)])
        if len(sale_order_ids)>0:
            for sale_order_id in sale_order_ids:
                sale_order_id.uuid = uuid.uuid4()
    
    @api.multi    
    def cron_sale_order_send_sns_custom(self, cr=None, uid=False, context=None):
        sale_order_ids = self.env['sale.order'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('sent', 'sale', 'done'))
            ]
        )
        if len(sale_order_ids)>0:
            _logger.info('Total='+str(len(sale_order_ids)))
            for sale_order_id in sale_order_ids:
                _logger.info('Enviando SNS '+str(sale_order_id.id))
                sale_order_id.action_send_sns(False)
    
    @api.multi    
    def cron_sale_order_upload_to_s3_generate(self, cr=None, uid=False, context=None):
        sale_order_ids = self.env['sale.order'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('sent', 'sale', 'done'))
            ]
        )
        if len(sale_order_ids)>0:
            _logger.info(len(sale_order_ids))            
            for sale_order_id in sale_order_ids:
                _logger.info('Generando presupuesto '+str(sale_order_id.id))
                #sale_order_id.action_upload_pdf_to_s3()
                sale_order_id.action_send_sns(False)
                    
    @api.one
    def action_upload_pdf_to_s3(self):
        if self.state in ['sent', 'sale', 'done']:
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
            report_sale_pdf_content = self.env['report'].get_pdf([self.id], 'sale.report_saleorder')
            #put_object        
            response_put_object = s3.put_object(Body=report_sale_pdf_content, Bucket=s3_bucket_docs_oniad_com, Key='sale-order/'+str(self.uuid)+'.pdf')

    @api.multi
    def action_send_sns_multi(self):
        for item in self:
            _logger.info('Enviando SNS ' + str(item.id))
            item.action_send_sns(False)

    @api.one
    def action_send_sns(self, regenerate_pdf=True):
        if self.state in ['sent', 'sale', 'done']:
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
                'name': str(self.name),
                'currency': str(self.currency_id.name),
                'state': str(self.state),
                'create_date': str(self.create_date),
                'date_order': str(self.date_order),                
                'amount_untaxed': self.amount_untaxed,
                'amount_tax': self.amount_tax,
                'amount_total': self.amount_total,
                'url_pdf': 'https://docs.oniad.com/sale-order/'+str(self.uuid)+'.pdf',
                's3_pdf': str(s3_bucket_docs_oniad_com)+'/sale-order/'+str(self.uuid)+'.pdf',
                'order_line': []
            }
            #order_line
            if len(self.order_line)>0:
                for order_line_item in self.order_line:
                    message_order_line_id = {
                        'name': str(order_line_item.name.encode('utf-8')),
                        'product_uom_qty': order_line_item.product_uom_qty,
                        'price_unit': order_line_item.price_unit,
                        'price_subtotal': order_line_item.price_unit,
                        'discount': order_line_item.price_unit,
                        'oniad_transaction_id': int(order_line_item.oniad_transaction_id.id)
                    }
                    message['order_line'].append(message_order_line_id)
            #enviroment
            enviroment = 'dev'
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if '//erp.oniad.com' in web_base_url:
                enviroment = 'prod'                    
            #sns_name            
            sns_name = 'oniad-platform-command-odoo-sale-order'
            if enviroment=='dev':
                sns_name = 'oniad-platform_dev-command-odoo-sale-order'
            #publish
            response = sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:534422648921:'+str(sns_name),
                Message=json.dumps(message, indent=2),
                MessageAttributes={
                    'Headers': {
                        'DataType': 'String',
                        'StringValue': json.dumps([{'type': 'Oniad\\Domain\\Odoo\\OdooSaleOrderAvailableEvent'},[]])
                    }
                }                                
            )
            if 'MessageId' not in response:
                action_response = False        
            #return
            return action_response
    
    @api.one
    def write(self, vals):      
        #super                                                               
        return_object = super(SaleOrder, self).write(vals)
        #check_if_paid
        if vals.get('state')=='sent':
            #action_send_sns
            self.action_send_sns(True)
        #return
        return return_object                    