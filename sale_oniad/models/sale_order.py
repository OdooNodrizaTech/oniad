# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields, tools
import uuid
import boto3
import json
_logger = logging.getLogger(__name__)


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

    @api.model
    def cron_sale_order_uuid_generate(self):
        order_ids = self.env['sale.order'].search(
            [
                ('uuid', '=', False)
            ]
        )
        if order_ids:
            for order_id in order_ids:
                order_id.uuid = uuid.uuid4()

    @api.model
    def cron_sale_order_send_sns_custom(self):
        order_ids = self.env['sale.order'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('sent', 'sale', 'done'))
            ]
        )
        if order_ids:
            _logger.info('Total=%s' % len(order_ids))
            for order_id in order_ids:
                _logger.info('Enviando SNS %s ' % order_id.id)
                order_id.action_send_sns(False)

    @api.model
    def cron_sale_order_upload_to_s3_generate(self):
        order_ids = self.env['sale.order'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('sent', 'sale', 'done'))
            ]
        )
        if order_ids:
            _logger.info(len(order_ids))
            for order_id in order_ids:
                _logger.info('Generando presupuesto %s' % order_id.id)
                # sale_order_id.action_upload_pdf_to_s3()
                order_id.action_send_sns(False)

    @api.multi
    def action_upload_pdf_to_s3(self):
        for item in self:
            if item.state in ['sent', 'sale', 'done']:
                # define
                AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
                AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
                s3_bucket_docs_oniad_com = tools.config.get('s3_bucket_docs_oniad_com')
                # boto3
                s3 = boto3.client(
                    's3',
                    region_name=AWS_SMS_REGION_NAME,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                )
                # get_pdf
                pdf_item = self.env.ref(
                    'sale.action_report_saleorder'
                ).sudo().render_qweb_pdf([item.id])[0]
                # put_object
                s3.put_object(
                    Body=pdf_item,
                    Bucket=s3_bucket_docs_oniad_com,
                    Key='sale-order/%s.pdf' % item.uuid
                )

    @api.multi
    def action_send_sns_multi(self):
        for item in self:
            _logger.info('Enviando SNS %s' % item.id)
            item.action_send_sns(False)

    @api.multi
    def action_send_sns(self, regenerate_pdf=True):
        self.ensure_one()
        if self.state in ['sent', 'sale', 'done']:
            action_response = True
            # action_upload_pdf_to_s3
            if regenerate_pdf:
                self.action_upload_pdf_to_s3()
            # define
            AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
            AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
            AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
            s3_bucket_docs_oniad_com = tools.config.get('s3_bucket_docs_oniad_com')
            # boto3
            sns = boto3.client(
                'sns',
                region_name=AWS_SMS_REGION_NAME,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            # message
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
                'url_pdf': 'https://docs.oniad.com/sale-order/%s.pdf' % self.uuid,
                's3_pdf': '%s/sale-order/%s.pdf' % (
                    s3_bucket_docs_oniad_com,
                    self.uuid
                ),
                'order_line': []
            }
            # order_line
            if self.order_line:
                for line_item in self.order_line:
                    message_order_line_id = {
                        'name': str(line_item.name.encode('utf-8')),
                        'product_uom_qty': line_item.product_uom_qty,
                        'price_unit': line_item.price_unit,
                        'price_subtotal': line_item.price_unit,
                        'discount': line_item.price_unit,
                        'oniad_transaction_id': int(line_item.oniad_transaction_id.id)
                    }
                    message['order_line'].append(message_order_line_id)
            # enviroment
            enviroment = 'dev'
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if '//erp.oniad.com' in base_url:
                enviroment = 'prod'
            # sns_name
            sns_name = 'oniad-platform-command-odoo-sale-order'
            if enviroment == 'dev':
                sns_name = 'oniad-platform_dev-command-odoo-sale-order'
            # publish
            header_value = 'Oniad\\Domain\\Odoo\\OdooSaleOrderAvailableEvent'
            response = sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:534422648921:'+str(sns_name),
                Message=json.dumps(message, indent=2),
                MessageAttributes={
                    'Headers': {
                        'DataType': 'String',
                        'StringValue': json.dumps([{'type': header_value}, []])
                    }
                }
            )
            if 'MessageId' not in response:
                action_response = False
            # return
            return action_response

    @api.multi
    def write(self, vals):
        # super
        return_object = super(SaleOrder, self).write(vals)
        # check_if_paid
        if vals.get('state') == 'sent':
            # action_send_sns
            self.action_send_sns(True)
        # return
        return return_object
