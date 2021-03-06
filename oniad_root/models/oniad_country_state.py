# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools, _
import json
import logging
import boto3
_logger = logging.getLogger(__name__)


class OniadCountryState(models.Model):
    _name = 'oniad.country.state'
    _description = 'Oniad Country State'

    name = fields.Char(
        string='Name'
    )
    iso_code = fields.Char(
        string='Iso Code'
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State'
    )
    oniad_country_id = fields.Many2one(
        comodel_name='oniad.country',
        string='Oniad Country'
    )
    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Posicion fiscal'
    )

    @api.model
    def cron_sqs_oniad_country_state(self):
        _logger.info('cron_sqs_oniad_country_state')
        sqs_oniad_country_state_url = tools.config.get('sqs_oniad_country_state_url')
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
                QueueUrl=sqs_oniad_country_state_url,
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
                                _('The field does not exist %s') % fnc
                    # operations
                    if result_message['statusCode'] == 200:
                        previously_found = False
                        id_item = int(message_body['id'])
                        items = self.env['oniad.country.state'].search(
                            [
                                ('id', '=', id_item)
                            ]
                        )
                        if items:
                            previously_found = True
                        # params
                        data = {
                            'name': str(message_body['name'].encode('utf-8')),
                            'iso_code': str(message_body['iso_code']),
                            'oniad_country_id': int(message_body['country_id']),
                            'fiscal_position_id': 1,
                        }
                        # oniad_country_id
                        if 'oniad_country_id' in data:
                            if data['oniad_country_id'] > 0:
                                country_ids = self.env['oniad.country'].search(
                                    [
                                        ('id', '=', int(data['oniad_country_id']))
                                    ]
                                )
                                if country_ids:
                                    data['country_id'] = country_ids[0].country_id.id
                                    # search_state_id
                                    if '-' in data['iso_code']:
                                        iso_code_split = data['iso_code'].split('-')
                                        state_ids = self.env[
                                            'res.country.state'
                                        ].search(
                                            [
                                                ('code', '=', str(iso_code_split[1])),
                                                (
                                                    'country_id',
                                                    '=',
                                                    country_ids[0].country_id.id
                                                )
                                            ]
                                        )
                                        if len(state_ids) > 0:
                                            data['state_id'] = state_ids[0].id
                                else:
                                    result_message['statusCode'] = 500
                                    result_message['return_body'] = \
                                        _('Country_id=%s does not exist') \
                                        % data['oniad_country_id']
                        # add_id
                        if not previously_found:
                            data['id'] = int(message_body['id'])
                        # final_operations
                        _logger.info(data)
                        # create-write
                        if not previously_found:
                            items[0].write(data)
                        else:
                            self.env['oniad.country.state'].sudo().create(data)
                    # final_operations
                    result_message['data'] = data
                    _logger.info(result_message)
                    # remove_message
                    if result_message['statusCode'] == 200:
                        sqs.delete_message(
                            QueueUrl=sqs_oniad_country_state_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
