# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools, _

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz
import dateutil.parser
import json
import logging
import boto3
_logger = logging.getLogger(__name__)


class OniadUser(models.Model):
    _name = 'oniad.user'
    _description = 'Oniad User'
    _rec_name = 'id'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency'
    )
    lang = fields.Char(
        string='Lang'
    )
    name = fields.Char(
        string='Name'
    )
    last_name = fields.Char(
        string='Lastname'
    )
    uuid = fields.Char(
        string='Uuid'
    )
    email = fields.Char(
        string='Email'
    )
    phone = fields.Char(
        string='Phone'
    )
    iso_code = fields.Char(
        string='Iso Code'
    )
    timezone = fields.Char(
        string='Timezone'
    )
    confirmed = fields.Boolean(
        string='Confirmed'
    )
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        string='Oniad address'
    )
    oniad_accountmanager_id = fields.Many2one(
        comodel_name='oniad.accountmanager',
        string='Oniad Account Manager'
    )
    parent_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Parent'
    )
    type = fields.Selection(
        selection=[
            ('user', 'User'),
            ('agency', 'Agency'),
            ('client_own', 'Client own'),
        ],
        string='Type',
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
    tag_ids = fields.One2many(
        'oniad.user.tag',
        'oniad_user_id',
        string='Tags'
    )
    oniad_user_id_link = fields.Char(
        compute='_compute_oniad_user_id_link',
        string='OniAd User',
        store=False
    )
    oniad_user_count = fields.Integer(
        compute='_compute_oniad_user_count',
        string="Oniad Users",
    )
    oniad_transaction_count = fields.Integer(
        compute='_compute_oniad_transaction_count',
        string="Oniad Transactions",
    )
    oniad_campaign_count = fields.Integer(
        compute='_compute_oniad_campaign_count',
        string="Oniad Campaigns",
    )
    crm_lead_opportunity_count = fields.Integer(
        compute='_compute_crm_lead_opportunity_count',
        string="Crm Leads",
    )

    @api.multi
    def _compute_oniad_user_id_link(self):
        for item in self:
            if item.id > 0:
                item.oniad_user_id_link = '%s/backend/admin/supadmin/card/%s' \
                                          % (
                                              'https://platform.oniad.com',
                                              item.id
                                          )

    @api.multi
    def _compute_oniad_user_count(self):
        for item in self:
            item.oniad_user_count = len(
                self.env['oniad.user'].search(
                    [
                        ('parent_id', '=', item.id)
                    ]
                )
            )

    @api.multi
    def _compute_oniad_transaction_count(self):
        for item in self:
            item.oniad_transaction_count = len(
                self.env['oniad.transaction'].search(
                    [
                        ('oniad_user_id', '=', item.id)
                    ]
                )
            )

    @api.multi
    def _compute_oniad_campaign_count(self):
        for item in self:
            item.oniad_campaign_count = len(
                self.env['oniad.campaign'].search(
                    [
                        ('oniad_user_id', '=', item.id)
                    ]
                )
            )

    @api.multi
    @api.depends('partner_id')
    def _compute_crm_lead_opportunity_count(self):
        for item in self:
            item.crm_lead_opportunity_count = len(
                self.env['crm.lead'].search(
                    [
                        ('type', '=', 'opportunity'),
                        ('partner_id', '=', item.partner_id.id)
                    ]
                )
            )

    @api.multi
    def check_res_partner(self):
        self.ensure_one()
        vals = {
            'oniad_user_id': self.id,
            'name': self.email,
            'customer': True,
            'email': self.email,
            'lang': str(self.lang)
        }
        # name
        if self.name and self.name != '':
            vals['name'] = self.name
        # lastname
        if self.last_name:
            vals['name'] = "%s %s" % (
                self.name,
                self.last_name
            )
        # phone
        if self.phone:
            first_char_phone = self.phone[:1]
            mobile_first_chars = [6, 7]
            if first_char_phone in mobile_first_chars:
                vals['mobile'] = self.phone
            else:
                vals['phone'] = self.phone
        # oniad_accountmanager_id
        if self.oniad_accountmanager_id.user_id:
            vals['user_id'] = self.oniad_accountmanager_id.user_id.id
        # operations
        if self.partner_id.id == 0:
            need_create_partner = True
            # convert lead to opportunity
            if self.odoo_lead and self.odoo_lead != '':
                need_create_partner = False
                # search
                lead_ids = self.env['crm.lead'].search(
                    [
                        ('register_token', '=', self.odoo_lead)
                    ]
                )
                if lead_ids:
                    for lead_id in lead_ids:
                        if lead_id.type == 'lead':
                            # convert_opportunity_create_partner
                            lead_id.convert_opportunity_create_partner(
                                False,
                                False
                            )
                            # need_update?
                            if lead_id.partner_id:
                                self.partner_id = lead_id.partner_id.id
                            else:
                                need_create_partner = True
            # create
            if need_create_partner:
                partner_obj = self.env['res.partner'].sudo().create(
                    vals
                )
                if partner_obj.id > 0:
                    self.partner_id = partner_obj.id
        else:
            self.partner_id.update(vals)
        # Fix define_user_id_in_res_partner
        if self.oniad_address_id:
            self.oniad_address_id.define_user_id_in_res_partner()

    @api.multi
    def check_sleep_lead(self):
        self.ensure_one()
        if self.create_date >= '2020-01-12':
            if self.tag_ids:
                user_dormido = False
                if self.tag_ids:
                    for tag_id in self.tag_ids:
                        if tag_id.tag == 'ESTADO_DORMIDO':
                            user_dormido = True
                # user_dormido
                if user_dormido:
                    lead_ids = self.env['crm.lead'].search(
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
                    if len(lead_ids) == 0:
                        # crm_lead_vals
                        vals = {
                            'partner_id': self.partner_id.id,
                            'lead_oniad_type': 'sleep',
                            'type': 'opportunity',
                            'commercial_activity_type': 'account',
                            'active': True,
                            'probability': 10,
                            'team_id': 1,
                            'stage_id': 1,
                            'name': 'Cliente dormid',
                            'description': 'Despertar al cliente',
                            'color': 5
                        }
                        # phone
                        if self.phone:
                            vals['phone'] = str(self.phone)
                        # user_id
                        if self.oniad_accountmanager_id:
                            if self.oniad_accountmanager_id.user_id:
                                vals['user_id'] = \
                                    self.oniad_accountmanager_id.user_id.id
                        # create
                        if 'user_id' in vals:
                            self.env['crm.lead'].sudo(vals['user_id']).create(vals)
                        else:
                            self.env['crm.lead'].sudo().create(vals)

    @api.model
    def create(self, values):
        return_item = super(OniadUser, self).create(values)
        # operations
        return_item.check_res_partner()
        # return
        return return_item

    @api.multi
    def write(self, vals):
        # user_id_old
        user_id_old = 0
        if self.partner_id:
            if self.partner_id.user_id:
                user_id_old = self.partner_id.user_id.id
        # write
        return_write = super(OniadUser, self).write(vals)
        # operations
        self.check_res_partner()
        # self.check_sleep_lead()
        # user_id_new
        user_id_new = 0
        if self.partner_id:
            if self.partner_id.user_id:
                user_id_new = self.partner_id.user_id.id
        # reasign_crm_leads
        if user_id_new > 0:
            if user_id_old != user_id_new:
                self.reasign_crm_leads()
        # return
        return return_write

    @api.multi
    def reasign_crm_leads(self):
        for item in self:
            if item.partner_id:
                if item.partner_id.user_id:
                    lead_ids = self.env['crm.lead'].search(
                        [
                            ('partner_id', '=', item.partner_id.id),
                            ('type', '=', 'opportunity'),
                            ('active', '=', True),
                            ('probability', '>', 0),
                            ('probability', '<', 100)
                        ]
                    )
                    if lead_ids:
                        for lead_id in lead_ids:
                            lead_id.user_id = item.partner_id.user_id.id
                            followers_ids = self.env['mail.followers'].search(
                                [
                                    ('res_model', '=', 'crm.lead'),
                                    ('res_id', '=', lead_id.id)
                                ]
                            )
                            if followers_ids:
                                for fi in followers_ids:
                                    if fi.partner_id.id != lead_id.partner_id.id:
                                        fi.unlink()
                            # add_new (user_id)
                            vals = {
                                'res_model': 'crm.lead',
                                'res_id': lead_id.id,
                                'partner_id': lead_id.user_id.partner_id.id,
                                'subtype_ids': [(4, [1])]
                            }
                            self.env['mail.followers'].sudo().create(vals)

    @api.model
    def cron_sqs_oniad_user(self):
        _logger.info('cron_sqs_oniad_user')
        sqs_oniad_user_url = tools.config.get('sqs_oniad_user_url')
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
                QueueUrl=sqs_oniad_user_url,
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
                    # result_message
                    result_message = {
                        'statusCode': 200,
                        'return_body': 'OK',
                        'message': message_body
                    }
                    # fields_need_check
                    fields_need_check = ['id']
                    for fnc in fields_need_check:
                        if fnc not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = \
                                _('The field does not exist %s') %fnc
                    # operations
                    if result_message['statusCode'] == 200:
                        previously_found = False
                        id_item = int(message_body['id'])
                        user_ids = self.env['oniad.user'].search(
                            [
                                ('id', '=', id_item)
                            ]
                        )
                        if user_ids:
                            previously_found = True
                        # params
                        vals = {
                            'currency_id': 1,
                            'lang': str(message_body['lang']),
                            'uuid': str(message_body['uuid']),
                            'email': str(message_body['email']),
                            'iso_code': str(message_body['iso_code']),
                            'confirmed': str(message_body['confirmed']),
                            'type': 'user',
                            'oniad_managed': str(message_body['oniad_managed'])
                        }
                        # name
                        try:
                            vals['name'] = str(message_body['name'].encode('utf-8'))
                        except:
                            vals['name'] = str(message_body['name'])
                        # created_at
                        if 'created_at' in message_body:
                            if message_body['created_at'] is not None:
                                created_at = dateutil.parser.parse(
                                    str(message_body['created_at'])
                                )
                                created_at = \
                                    created_at.replace() - created_at.utcoffset()
                                vals['create_date'] = \
                                    created_at.strftime("%Y-%m-%d %H:%M:%S")
                        # last_login
                        if 'last_login' in message_body:
                            if message_body['last_login'] is not None:
                                if message_body['last_login'] != '':
                                    last_login = dateutil.parser.parse(
                                        str(message_body['last_login'])
                                    )
                                    last_login = \
                                        last_login.replace() - last_login.utcoffset()
                                    vals['last_login'] = \
                                        last_login.strftime("%Y-%m-%d %H:%M:%S")
                        # fields_need_check
                        fields_need_check = [
                            'last_name', 'phone', 'timezone', 'parent_id', 'confirmed'
                        ]
                        for fnc in fields_need_check:
                            if fnc in message_body:
                                if message_body[fnc] != '':
                                    if message_body[fnc] is not None:
                                        if field_need_check in ['last_name']:
                                            try:
                                                vals[fnc] = str(message_body[fnc].encode('utf-8'))
                                            except:
                                                vals[fnc] = str(message_body[fnc])
                                        else:
                                            vals[fnc] = str(message_body[fnc])
                        # parent_id
                        if 'parent_id' in data_oniad_user:
                            if vals['parent_id'] == '0':
                                del vals['parent_id']
                        # check parent_id exists
                        if 'parent_id' in data_oniad_user:
                            oniad_user_ids = self.env['oniad.user'].search(
                                [
                                    ('id', '=', vals['parent_id'])
                                ]
                            )
                            if len(oniad_user_ids) == 0:
                                result_message['statusCode'] = 500
                                result_message['return_body'] = \
                                    _('User (parent_id) %s does not exist') % vals['parent_id']
                        # address_id
                        if 'address_id' in message_body:
                            if message_body['address_id'] != '':
                                if message_body['address_id'] is not None:
                                    if int(message_body['address_id']) != 0:
                                        vals['oniad_address_id'] = int(message_body['address_id'])
                        # accountmanager_id
                        if 'accountmanager_id' in message_body:
                            if message_body['accountmanager_id'] != '':
                                if message_body['accountmanager_id'] is not None:
                                    if int(message_body['accountmanager_id']) != 0:
                                        vals['oniad_accountmanager_id'] = int(message_body['accountmanager_id'])
                        # type
                        if 'roles' in message_body:
                            # ROLE_CLIENT_OWN
                            if 'ROLE_CLIENT_OWN' in message_body['roles']:
                                vals['type'] = 'client_own'
                            # ROLE_AGENCY
                            if 'ROLE_AGENCY' in message_body['roles']:
                                vals['type'] = 'agency'
                        # spent
                        if 'spent' in message_body:
                            if message_body['spent'] is not None:
                                # cost
                                if message_body['spent']['cost'] is not None:
                                    vals['spent_cost'] = message_body['spent']['cost']
                                # min_date
                                if message_body['spent']['min_date'] is not None:
                                    vals['spent_min_date'] = message_body['spent']['min_date']
                                # max_date
                                if message_body['spent']['max_date'] is not None:
                                    vals['spent_max_date'] = message_body['spent']['max_date']
                        # boolean_fields
                        boolean_fields = ['confirmed', 'oniad_managed']
                        for bf in boolean_fields:
                            if bf in vals:
                                if vals[bf] == 'True':
                                    vals[bf] = True
                                elif vals[bf] == 'False':
                                    vals[bf] = False
                                else:
                                    vals[bf]
                        # odoo_lead
                        if 'context' in message_body:
                            if message_body['context'] != '':
                                if message_body['context'] is not None:
                                    if 'odoo_lead' in message_body['context']:
                                        if message_body['context']['odoo_lead'] != '':
                                            if message_body['context']['odoo_lead'] is not None:
                                                vals['odoo_lead'] = str(message_body['context']['odoo_lead'])
                        # add_id
                        if not previously_found:
                            vals['id'] = int(message_body['id'])
                        # search oniad_address_id (prevent errors)
                        if 'oniad_address_id' in vals:
                            if vals['oniad_address_id'] > 0:
                                address_ids = self.env['oniad.address'].search(
                                    [
                                        ('id', '=', int(vals['oniad_address_id']))
                                    ]
                                )
                                if len(address_ids) == 0:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = \
                                        _('Address %s does not exist') \
                                        % data_oniad_user['oniad_address_id']
                        # final_operations
                        result_message['data'] = vals
                        _logger.info(result_message)
                        # create-write
                        if result_message['statusCode'] == 200:
                            if previously_found:
                                user_ids[0].write(vals)
                            else:
                                self.env['oniad.user'].sudo().create(vals)

                    # remove_message
                    if result_message['statusCode'] == 200:
                        sqs.delete_message(
                            QueueUrl=sqs_oniad_user_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                
    @api.model
    def cron_sqs_oniad_usertag(self):
        _logger.info('cron_sqs_oniad_usertag')
        sqs_oniad_usertag_url = tools.config.get('sqs_oniad_usertag_url')
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
                QueueUrl=sqs_oniad_usertag_url,
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
                    # result_message
                    result_message = {
                        'statusCode': 200,
                        'return_body': 'OK',
                        'message': message_body
                    }
                    # general
                    # fields_need_check
                    fields_need_check = ['id', 'tags']
                    for fnc in fields_need_check:
                        if fnc not in message_body:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = \
                                _('The field% s does not exist') % fnc
                    # operations
                    if result_message['statusCode'] == 200:
                        item_id = int(message_body['id'])
                        user_ids = self.env['oniad.user'].search(
                            [
                                ('id', '=', item_id)
                            ]
                        )
                        if user_ids:
                            user_id = user_ids[0]
                            # tag_ids
                            if len(message_body['tags']) > 0:
                                tag_ids_real = []
                                for tag in message_body['tags']:
                                    tag_ids = self.env['oniad.user.tag'].search(
                                        [
                                            ('tag', '=', str(tag))
                                        ]
                                    )
                                    if tag_ids:
                                        tag_ids_real.append(int(tag_ids[0].id))
                                        # update
                                result_message['tag_ids'] = tag_ids_real
                                user_id.tag_ids = [(6, 0, tag_ids_real)]
                        else:
                            result_message['statusCode'] = 500
                            result_message['return_body'] = \
                                _('User_id=%s not found') % item_id

                    # final_operations
                    _logger.info(result_message)                                
                    # remove_message
                    if result_message['statusCode'] == 200:
                        sqs.delete_message(
                            QueueUrl=sqs_oniad_usertag_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )        
        
    @api.model
    def cron_oniad_user_auto_generate_welcome_lead_id(self):
        _logger.info('cron_oniad_user_auto_generate_welcome_lead_id')
        current_date = datetime.today()
        start_date = current_date + relativedelta(days=-8)
        end_date = current_date
        user_ids = self.env['oniad.user'].search(
            [
                ('partner_id', '!=', False),
                ('partner_id.user_id', '!=', False),
                ('type', 'in', ('user', 'agency')),
                ('welcome_lead_id', '=', False),
                ('create_date', '>=', start_date.strftime("%Y-%m-%d")),
                ('create_date', '<=', end_date.strftime("%Y-%m-%d"))
            ]
        )    
        if user_ids:
            _logger.info(len(user_ids))
            for user_id in user_ids:
                user_id.action_generate_welcome_lead()
                
    @api.multi
    def action_generate_welcome_lead(self):
        for item in self:
            if self.welcome_lead_id.id == 0:
                if self.type in ['user', 'agency']:
                    if self.partner_id:
                        if self.partner_id.user_id:
                            if self.create_date.strftime("%Y-%m-%d") >= '2020-02-12':
                                # define
                                current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                                mail_activity_date_deadline = current_date + relativedelta(days=7)
                                # need_check
                                need_check = False
                                if self.phone:
                                    need_check = True
                                else:
                                    diff = \
                                        datetime.strptime(
                                            str(current_date.strftime("%Y-%m-%d %H:%M:%S")),
                                            '%Y-%m-%d %H:%M:%S'
                                        ) - \
                                        datetime.strptime\
                                            (str(self.create_date.strftime("%Y-%m-%d %H:%M:%S")),
                                             '%Y-%m-%d %H:%M:%S'
                                             )
                                    dateTimeDifferenceInHours = diff.total_seconds() / 3600
                                    if dateTimeDifferenceInHours >= 1 and dateTimeDifferenceInHours < 200:
                                        need_check = True
                                if need_check:
                                    lead_ids = self.env['crm.lead'].search(
                                        [
                                            ('partner_id', '=', self.partner_id.id),
                                            ('lead_oniad_type', '=', 'welcome'),
                                            ('type', '=', 'opportunity'),
                                            ('commercial_activity_type', '=', 'account')
                                        ]
                                    )
                                    if lead_ids:
                                        self.welcome_lead_id = lead_ids[0].id
                                    else:
                                        template_id = int(
                                            self.env[
                                                'ir.config_parameter'
                                            ].sudo().get_param('oniad_welcome_lead_template_id')
                                        )
                                        # es necesario crear lead
                                        vals = {
                                            'partner_id': self.partner_id.id,
                                            'lead_oniad_type': 'welcome',
                                            'type': 'opportunity',
                                            'commercial_activity_type': 'account',
                                            'active': True,
                                            'probability': 10,
                                            'team_id': 1,
                                            'stage_id': 1,
                                            'name': 'Hola, quiero ayudarte a mejorar tus campañas',
                                            'description': 'Presentarse y ayudar a nuevos clientes',
                                            'color': 5
                                        }
                                        # phone
                                        if self.phone:
                                            vals['phone'] = str(self.phone)
                                        # user_id
                                        if self.oniad_accountmanager_id:
                                            if self.oniad_accountmanager_id.user_id:
                                                vals['user_id'] = self.oniad_accountmanager_id.user_id.id
                                        # create
                                        if 'user_id' in crm_lead_vals:
                                            lead_obj = self.env['crm.lead'].sudo(
                                                vals['user_id']
                                            ).create(vals)
                                        else:
                                            lead_obj = self.env['crm.lead'].sudo().create(vals)
                                        # si corresponde enviamos un email
                                        if 'phone' not in crm_lead_vals:
                                            # enviamos_email
                                            lead_obj.action_send_mail_with_template_id(template_id)
                                            # update
                                            lead_obj.stage_id = 2
                                        # mail_activity
                                        if 'user_id' in crm_lead_vals:
                                            ir_model_ids = self.env['ir.model'].search(
                                                [
                                                    ('model', '=', 'crm.lead')
                                                ]
                                            )
                                            if ir_model_ids:
                                                ir_model_item = ir_model_ids[0]
                                                # vals
                                                vals = {
                                                    'active': True,
                                                    'res_model': ir_model_item.model,
                                                    'res_model_id': ir_model_item.id,
                                                    'res_id': crm_lead_obj.id,
                                                    'activity_type_id': 3,
                                                    'user_id': vals['user_id'],
                                                    'date_deadline':
                                                        mail_activity_date_deadline.strftime("%Y-%m-%d"),
                                                    'summary': 'Revisar contacto usuario'
                                                }
                                                self.env['mail.activity'].sudo(vals['user_id']).create(vals)
                                        # update
                                        self.welcome_lead_id = lead_obj.id
