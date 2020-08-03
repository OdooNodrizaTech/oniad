# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools, _
import json
import logging
import boto3
_logger = logging.getLogger(__name__)


class OniadCountry(models.Model):
    _name = 'oniad.country'
    _description = 'Oniad Country'

    name = fields.Char(
        string='Name'
    )
    iso_code = fields.Char(
        string='Iso Code'
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country'
    )
    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Fiscal position',
        help='This fiscal position will only be used when the address '
             'has no province, otherwise the fiscal fiscal position '
             'of the province will be used'
    )

    @api.model
    def cron_sqs_oniad_country(self):
        _logger.info('cron_sqs_oniad_country')
        sqs_oniad_country_url = tools.config.get('sqs_oniad_country_url')
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
                QueueUrl=sqs_oniad_country_url,
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
                        oniad_country_ids = self.env['oniad.country'].search(
                            [
                                ('id', '=', id_item)
                            ]
                        )
                        if oniad_country_ids:
                            previously_found = True
                        # params
                        data_oniad_country = {
                            'name': str(message_body['name'].encode('utf-8')),
                            'iso_code': str(message_body['iso_code'])
                        }
                        # Fix iso_code
                        res_country_ids = self.env['res.country'].search(
                            [
                                ('code', '=', str(data_oniad_country['iso_code']))
                            ]
                        )
                        if res_country_ids:
                            data_oniad_country['country_id'] = res_country_ids[0].id
                        # add_id
                        if not previously_found:
                            data_oniad_country['id'] = int(message_body['id'])
                        # final_operations
                        _logger.info(data_oniad_country)
                        # create-write
                        if previously_found:
                            oniad_country_id = oniad_country_ids[0]
                            # write
                            oniad_country_id.write(data_oniad_country)
                        else:
                            self.env['oniad.country'].sudo().create(data_oniad_country)
                    # final_operations
                    result_message['data'] = data_oniad_country
                    _logger.info(result_message)
                    # remove_message
                    if result_message['statusCode'] == 200:
                        sqs.delete_message(
                            QueueUrl=sqs_oniad_country_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
