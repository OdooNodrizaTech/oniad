# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools, _
import json
import logging
import boto3
_logger = logging.getLogger(__name__)


class OniadAddress(models.Model):
    _name = 'oniad.address'
    _description = 'Oniad Address'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto'
    )
    oniad_country_id = fields.Many2one(
        comodel_name='oniad.country',
        string='Oniad Country'
    )
    oniad_country_state_id = fields.Many2one(
        comodel_name='oniad.country.state',
        string='Oniad Country State'
    )
    name = fields.Char(
        string='Nombre'
    )
    cp = fields.Char(
        string='Codigo postal'
    )
    cif = fields.Char(
        string='Cif'
    )
    iva = fields.Float(
        string='Iva'
    )
    city = fields.Char(
        string='Ciudad'
    )
    phone = fields.Char(
        string='Telefono'
    )
    address = fields.Char(
        string='Direccion'
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Pais'
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Provincia'
    )
    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Posicion fiscal'
    )
    a_number = fields.Char(
        string='A number'
    )
    res_partner_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Cuenta bancaria'
    )
    oniad_transaction_count = fields.Integer(
        compute='_compute_oniad_transaction_count',
        string="Oniad Transactions",
    )
    sale_order_count = fields.Integer(
        compute='_compute_sale_order_count',
        string="Sale Orders",
    )
    account_invoice_count = fields.Integer(
        compute='_compute_account_invoice_count',
        string="Account Invoices",
    )

    @api.multi
    @api.depends('oniad_address_id')
    def _compute_oniad_transaction_count(self):
        for item in self:
            item.oniad_transaction_count = len(
                self.env['oniad.transaction'].search(
                    [
                        ('oniad_address_id', '=', item.id)
                    ]
                )
            )

    @api.multi
    @api.depends('partner_id')
    def _compute_sale_order_count(self):
        for item in self:
            item.sale_order_count = 0
            if item.partner_id:
                _logger.info(item.partner_id.id)
                item.sale_order_count = len(
                    self.env['sale.order'].search(
                        [
                            ('partner_invoice_id', '=', item.partner_id.id)
                        ]
                    )
                )

    @api.multi
    @api.depends('oniad_address_id')
    def _compute_account_invoice_count(self):
        for item in self:
            item.account_invoice_count = len(
                self.env['account.invoice'].search(
                    [
                        ('oniad_address_id', '=', item.id)
                    ]
                )
            )

    @api.model
    def check_vat_error(self, vat, id_item):
        _logger.info(
            _('The vat %s of the oniad_address_id =% s is incorrect')
            % (vat, id_item)
        )

    @api.multi
    def define_user_id_in_res_partner(self):
        for item in self:
            if item.partner_id:
                user_ids = self.env['oniad.user'].search(
                    [
                        ('oniad_address_id', '=', item.id)
                    ]
                )
                if user_ids:
                    user_id = user_ids[0]
                    if user_id.oniad_accountmanager_id:
                        if user_id.oniad_accountmanager_id.user_id:
                            item.partner_id.user_id = \
                                user_id.oniad_accountmanager_id.user_id.id

    @api.multi
    def check_res_partner(self):
        self.ensure_one()
        _logger.info('check_res_partner')
        # vals
        partner_vals = {
            'oniad_address_id': self.id,
            'name': self.name,
            'customer': True,
            'is_company': True,
            'country_id': self.country_id.id,
            'city': self.city,
            'street': self.address,
            'zip': self.cp,
            'state_id': self.state_id.id,
            'vat': "%s%s" % (
                self.country_id.code.upper(),
                self.cif
            ),
            'property_account_position_id': self.fiscal_position_id.id
        }
        # phone
        if self.phone:
            first_char_phone = self.phone[:1]
            mobile_first_chars = [6, 7]
            if first_char_phone in mobile_first_chars:
                partner_vals['mobile'] = self.phone
            else:
                partner_vals['phone'] = self.phone
        # operations
        if self.partner_id.id == 0:
            # customer_payment_mode_id
            partner_vals['customer_payment_mode_id'] = 1  # Transferencia
            # property_payment_term_id
            partner_vals['property_payment_term_id'] = 1  # Pago inmediato
            # check_if_need_create of previously exists
            vat_need_check = "%s%s" % (
                self.country_id.code,
                self.cif
            )
            res_partner_ids = self.env['res.partner'].search(
                [
                    ('is_company', '=', True),
                    ('vat', '=', vat_need_check)
                ]
            )
            if res_partner_ids:
                self.partner_id = res_partner_ids[0].id
            else:
                # create
                res_partner_obj = self.env['res.partner'].sudo().create(
                    partner_vals
                )
                if res_partner_obj:
                    self.partner_id = res_partner_obj.id
        else:
            # customer_payment_mode_id
            if self.partner_id.customer_payment_mode_id.id == 0:
                partner_vals['customer_payment_mode_id'] = 1  # Transferencia
            # property_payment_term_id
            if self.partner_id.property_payment_term_id.id == 0:
                partner_vals['property_payment_term_id'] = 1  # Pago inmediato
            # update
            self.partner_id.update(partner_vals)
        # define_user_id_in_res_partner
        self.define_user_id_in_res_partner()
        # res_partner_bank_id
        if self.a_number and self.res_partner_bank_id.id == 0:
            partner_bank_vals = {
                'acc_number': self.a_number,
                'partner_id': self.partner_id.id,
            }
            # search
            res_partner_bank_ids = self.env['res.partner.bank'].search(
                [
                    ('acc_number', '=', self.a_number)
                ]
            )
            if res_partner_bank_ids:
                _logger.info(
                    _('VERY STRANGE that this bank account already '
                      'exists to another client')
                )
            else:
                res_partner_bank_obj = self.env['res.partner.bank'].sudo().create(
                    partner_bank_vals
                )
                # update
                self.res_partner_bank_id = res_partner_bank_obj.id

    @api.model
    def create(self, values):
        return_item = super(OniadAddress, self).create(values)
        # operations
        return_item.check_res_partner()
        # return
        return return_item

    @api.multi
    def write(self, vals):
        return_write = super(OniadAddress, self).write(vals)
        # operations
        self.check_res_partner()
        # return
        return return_write

    @api.multi
    def action_send_sns(self):
        self.ensure_one()
        _logger.info('action_send_sns')

        action_response = True
        # define
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
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
            'payment_mode_id': {
                'id': int(self.partner_id.customer_payment_mode_id.id),
                'name': str(self.partner_id.customer_payment_mode_id.name)
            },
            'payment_term_id': {
                'id': int(self.partner_id.property_payment_term_id.id),
                'name': str(self.partner_id.property_payment_term_id.name)
            },
            'custom_day_due_1': int(self.partner_id.custom_day_due_1),
            'custom_day_due_2': int(self.partner_id.custom_day_due_2),
            'custom_day_due_3': int(self.partner_id.custom_day_due_3),
            'custom_day_due_4': int(self.partner_id.custom_day_due_4)
        }
        _logger.info(message)
        # enviroment
        enviroment = 'dev'
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if '//erp.oniad.com' in web_base_url:
            enviroment = 'prod'
        # sns_name
        sns_name = 'oniad-platform-command-odoo-oniad-address'
        if enviroment == 'dev':
            sns_name = 'oniad-platform_dev-command-odoo-oniad-address'
        # publish
        header_string = 'Oniad\\Domain\\Odoo\\OdooPaymentDataEvent'
        response = sns.publish(
            TopicArn='arn:aws:sns:eu-west-1:534422648921:'+str(sns_name),
            Message=json.dumps(message, indent=2),
            MessageAttributes={
                'Headers': {
                    'DataType': 'String',
                    'StringValue': json.dumps([{'type': header_string}, []])
                }
            }
        )
        if 'MessageId' not in response:
            action_response = False
        else:
            _logger.info(sns_name)
        # return
        return action_response

    @api.model
    def cron_sqs_oniad_address(self):
        _logger.info('cron_sqs_oniad_address')
        sqs_oniad_address_url = tools.config.get('sqs_oniad_address_url')
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')
        # boto3
        sqs = boto3.client(
            'sqs',
            region_name=AWS_SMS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        # Receive message from SQS queue
        total_messages = 10
        while total_messages > 0:
            response = sqs.receive_message(
                QueueUrl=sqs_oniad_address_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )
            if 'Messages' in response:
                total_messages = len(response['Messages'])
            else:
                total_messages = 0
            # continue
            if 'Messages' in response:
                for message in response['Messages']:
                    # message_body
                    message_body = json.loads(message['Body'])
                    # fix message
                    if 'Message' in message_body:
                        message_body = json.loads(message_body['Message'])
                    mb = message_body
                    # result_message
                    result_message = {
                        'statusCode': 200,
                        'return_body': 'OK',
                        'message': message_body
                    }
                    # fields_need_check
                    fields_need_check = ['id']
                    for field_need_check in fields_need_check:
                        if field_need_check not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = \
                                _('The field does not exist %s') \
                                % field_need_check
                    # operations
                    if result_message['statusCode'] == 200:
                        previously_found = False
                        id_item = int(message_body['id'])
                        oniad_address_ids = self.env['oniad.address'].search(
                            [
                                ('id', '=', id_item)
                            ]
                        )
                        if oniad_address_ids:
                            previously_found = True
                        # params
                        vals = {
                            'name': str(message_body['name'].encode('utf-8')),
                            'oniad_country_id': int(message_body['country_id']),
                            'oniad_country_state_id': int(message_body['state_id']),
                            'fiscal_position_id': 1
                        }
                        # fields_need_check
                        fnc_items = [
                            'cp', 'cif', 'iva', 'city', 'phone', 'address', 'a_number'
                        ]
                        for fnc in fnc_items:
                            if fnc in message_body:
                                if message_body[fnc] != '':
                                    if message_body[fnc] is not None:
                                        if field_need_check in ['city', 'address']:
                                            try:
                                                vals[fnc] = str(mb[fnc].encode('utf-8'))
                                            except:
                                                vals[fnc] = str(mb[fnc])
                                        else:
                                            vals[fnc] = str(mb[fnc])
                        # oniad_country_id
                        if 'oniad_country_id' in vals:
                            if vals['oniad_country_id'] > 0:
                                oniad_country_ids = self.env['oniad.country'].search(
                                    [
                                        ('id', '=', int(vals['oniad_country_id']))
                                    ]
                                )
                                if oniad_country_ids:
                                    oniad_country_id = oniad_country_ids[0]
                                    vals['country_id'] = \
                                        oniad_country_id.country_id.id
                                    vals['fiscal_position_id'] = \
                                        oniad_country_id.fiscal_position_id.id
                                else:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = \
                                        _('country_id=%s does not exist') \
                                        % vals['oniad_country_id']
                        # state_id
                        if 'oniad_country_state_id' in vals:
                            if vals['oniad_country_state_id'] > 0:
                                state_ids = self.env['oniad.country.state'].search(
                                    [
                                        (
                                            'id',
                                            '=',
                                            int(vals['oniad_country_state_id'])
                                        )
                                    ]
                                )
                                if state_ids:
                                    state_id = state_ids[0]
                                    vals['state_id'] = state_id.state_id.id
                                    vals['fiscal_position_id'] = \
                                        state_id.fiscal_position_id.id
                                else:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = \
                                        _('state_id=%s does not exist') \
                                        % vals['oniad_country_state_id']
                        # add_id
                        if not previously_found:
                            vals['id'] = int(message_body['id'])
                        # check_cif
                        vat_need_check = "%s%s" % (
                            message_body['country'].upper(),
                            vals['cif']
                        )
                        return_check_vat = self.partner_id.sudo().check_vat_custom(
                            vat_need_check
                        )
                        if not return_check_vat:
                            self.check_vat_error(vat_need_check, message_body['id'])
                            result_message['return_body'] = _('Error in CIF field')
                        else:
                            # final_operations
                            result_message['data'] = vals
                            _logger.info(result_message)
                            # create-write
                            if not previously_found:
                                self.env['oniad.address'].sudo().create(
                                    vals
                                )
                            else:
                                oniad_address_id = oniad_address_ids[0]
                                # write
                                oniad_address_id.write(vals)
                    # remove_message
                    if result_message['statusCode'] == 200:
                        sqs.delete_message(
                            QueueUrl=sqs_oniad_address_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
