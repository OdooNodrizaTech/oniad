# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import api, models, fields, tools, _
from odoo.exceptions import Warning as UserError
import uuid

import boto3
import json
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    margin = fields.Monetary(
        string='Margin'
    )
    # override date
    date = fields.Date(
        string='Date',
        copy=False,
        help="Leave empty to use the invoice date",
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

    @api.model
    def cron_account_invoice_uuid_generate(self):
        invoice_ids = self.env['account.invoice'].search(
            [
                ('uuid', '=', False)
            ]
        )
        if invoice_ids:
            for invoice_id in invoice_ids:
                invoice_id.uuid = uuid.uuid4()

    @api.model
    def cron_account_invoice_send_sns_custom(self):
        invoice_ids = self.env['account.invoice'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('open', 'paid')),
                ('type', 'in', ('out_invoice', 'out_refund')),
                ('date_invoice', '>=', '2020-01-01')
            ]
        )
        if invoice_ids:
            _logger.info('Total=%s' % len(invoice_ids))
            for invoice_id in invoice_ids:
                _logger.info('Enviando SNS %s' % invoice_id.id)
                invoice_id.action_send_sns(False)

    @api.model
    def cron_account_invoice_upload_to_s3_generate(self):
        invoice_ids = self.env['account.invoice'].search(
            [
                ('uuid', '!=', False),
                ('state', 'in', ('open', 'paid')),
                ('type', 'in', ('out_invoice', 'out_refund'))
            ]
        )
        if invoice_ids:
            _logger.info(len(invoice_ids))
            for invoice_id in invoice_ids:
                _logger.info('Generando factura %s' % invoice_id.id)
                # invoice_id.action_upload_pdf_to_s3()
                invoice_id.action_send_sns(False)

    @api.multi
    def action_upload_pdf_to_s3(self):
        for item in self:
            if item.state in ['open', 'paid']:
                if item.type in ['out_invoice', 'out_refund']:
                    # define
                    AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
                    AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
                    AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
                    s3_bucket = tools.config.get('s3_bucket_docs_oniad_com')
                    # boto3
                    s3 = boto3.client(
                        's3',
                        region_name=AWS_SMS_REGION_NAME,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                    )
                    try:
                        report_invoice_pdf_content = self.env.ref(
                            'account.account_invoices_without_payment'
                        ).sudo().render_qweb_pdf([item.id])[0]
                        # put_object
                        s3.put_object(
                            Body=report_invoice_pdf_content,
                            Bucket=s3_bucket,
                            Key='account-invoice/%s.pdf' % item.uuid
                        )
                    except:
                        _logger.info(
                            _('Errir al generar el PDF de la factura %s')
                            % item.id
                        )

    @api.multi
    def action_send_sns_multi(self):
        for item in self:
            _logger.info('Enviando SNS %s' % item.id)
            item.action_send_sns(False)

    @api.multi
    def action_send_sns(self, regenerate_pdf=True):
        self.ensure_one()
        if self.state in ['open', 'paid']:
            if self.type in ['out_invoice', 'out_refund']:
                action_response = True
                web_base_url = self.env[
                    'ir.config_parameter'
                ].sudo().get_param('web.base.url')
                # action_upload_pdf_to_s3
                if regenerate_pdf:
                    self.action_upload_pdf_to_s3()
                # define
                AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
                AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
                s3_bucket = tools.config.get('s3_bucket_docs_oniad_com')
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
                    'partner_max_credit_limit_allow':
                        self.partner_id.max_credit_limit_allow,
                    'url_pdf': 'https://docs.oniad.com/account-invoice/%s.pdf' % (
                        self.uuid
                    ),
                    's3_pdf': '%s/account-invoice/%s.pdf' % (
                        s3_bucket,
                        self.uuid
                    ),
                    'invoice_line_ids': [],
                    'tax_line_ids': [],
                    'payment_ids': []
                }
                # invoice_line_ids
                if self.invoice_line_ids:
                    for line_id in self.invoice_line_ids:
                        message_line_id = {
                            'name': str(line_id.name.encode('utf-8')),
                            'quantity': line_id.quantity,
                            'price_unit': line_id.price_unit,
                            'price_subtotal': line_id.price_unit,
                            'discount': line_id.price_unit,
                            'oniad_transaction_id':
                                int(line_id.oniad_transaction_id.id)
                        }
                        message['invoice_line_ids'].append(message_line_id)
                # tax_line_ids
                if self.tax_line_ids:
                    for tax_line_id in self.tax_line_ids:
                        message_tax_line_id = {
                            'name': str(tax_line_id.name.encode('utf-8')),
                            'base': tax_line_id.base,
                            'amount': tax_line_id.amount,
                        }
                        message['tax_line_ids'].append(message_tax_line_id)
                # payment_ids
                if self.payment_ids:
                    for payment_id in self.payment_ids:
                        message_payment_id = {
                            'id': int(payment_id.id),
                            'communication':
                                str(payment_id.communication.encode('utf-8')),
                            'payment_date': str(payment_id.payment_date),
                            'amount': payment_id.amount,
                            'oniad_transaction_id':
                                int(payment_id.oniad_transaction_id.id)
                        }
                        message['payment_ids'].append(message_payment_id)
                # enviroment
                enviroment = 'dev'
                if '//erp.oniad.com' in web_base_url:
                    enviroment = 'prod'
                # sns_name
                sns_name = 'oniad-platform-command-odoo-account-invoice'
                if enviroment == 'dev':
                    sns_name = 'oniad-platform_dev-command-odoo-account-invoice'
                # publish
                header_type = 'Oniad\\Domain\\Odoo\\OdooInvoiceAvailableEvent'
                response = sns.publish(
                    TopicArn='arn:aws:sns:eu-west-1:534422648921:%s' % sns_name,
                    Message=json.dumps(message, indent=2),
                    MessageAttributes={
                        'Headers': {
                            'DataType': 'String',
                            'StringValue': json.dumps(
                                [
                                    {
                                        'type': header_type
                                    }, []
                                ]
                            )
                        }
                    }
                )
                # logger
                _logger.info({
                    'enviroment': enviroment,
                    'sns_name': sns_name
                })
                # check
                if 'MessageId' not in response:
                    action_response = False
                else:
                    _logger.info(sns_name)
                # return
                return action_response

    @api.multi
    def action_calculate_margin(self):
        for item in self:
            if item.id:
                if item.invoice_line_ids:
                    margin_total = 0
                    for line_id in item.invoice_line_ids:
                        margin_total = margin_total + line_id.purchase_price

                    item.margin = margin_total

    @api.multi
    def write(self, vals):
        # super
        return_object = super(AccountInvoice, self).write(vals)
        # check_if_paid
        if vals.get('state') == 'paid':
            # action_send_sns
            self.action_send_sns(True)
        # return
        return return_object

    @api.multi
    def action_invoice_open(self):
        for item in self:
            if item.partner_id.vat:
                continue

            test_condition = (tools.config['test_enable'] and
                              not self.env.context.get('test_vat'))

            if test_condition:
                continue

            if item.partner_id.vat:
                raise UserError(
                    _('It is necessary to define a CIF / NIF '
                      'for the customer of the invoice')
                )
            elif item.type == "in_invoice" and not item.reference:
                raise UserError(
                    _('It is necessary to define a supplier '
                      'reference to validate the purchase invoice')
                )

        res = super(AccountInvoice, self).action_invoice_open()
        for item in self:
            item.action_calculate_margin()
            item.action_send_sns(True)
        # return
        return res

    @api.multi
    def action_auto_create_message_slack(self):
        self.ensure_one()
        super(
            AccountInvoice, self
        ).action_auto_create_message_slack()
        return False
