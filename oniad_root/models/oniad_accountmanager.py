# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools, _
import json
import logging
import boto3
_logger = logging.getLogger(__name__)


class OniadAccountmanager(models.Model):
    _name = 'oniad.accountmanager'
    _description = 'Oniad Accountmanager'
    _rec_name = 'email'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario'
    )
    email = fields.Char(
        string='Email'
    )

    @api.model
    def cron_sqs_oniad_accountmanager(self):
        _logger.info('cron_sqs_oniad_accountmanager')
        sqs_oniad_accountmanager_url = tools.config.get('sqs_oniad_accountmanager_url')
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
                QueueUrl=sqs_oniad_accountmanager_url,
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
                        accountmanager_ids = self.env['oniad.accountmanager'].search(
                            [
                                ('id', '=', id_item)
                            ]
                        )
                        if accountmanager_ids:
                            previously_found = True
                        # params
                        vals = {
                            'email': str(message_body['email'])
                        }
                        # add_id
                        if not previously_found:
                            vals['id'] = int(message_body['id'])
                        # final_operations
                        _logger.info(vals)
                        # create-write
                        if not previously_found:
                            self.env['oniad.accountmanager'].sudo().create(vals)
                        else:
                            # write
                            accountmanager_ids[0].write(vals)
                    # final_operations
                    result_message['data'] = vals
                    _logger.info(result_message)
                    # remove_message
                    if result_message['statusCode'] == 200:
                        sqs.delete_message(
                            QueueUrl=sqs_oniad_accountmanager_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )
