# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields, tools
import boto3, json
from botocore.exceptions import ClientError
_logger = logging.getLogger(__name__)


class OniadAddress(models.Model):
    _inherit = 'oniad.address'
    
    @api.model    
    def cron_oniad_address_credit_limit_send_sns_custom(self):
        address_ids = self.env['oniad.address'].search(
            [
                ('partner_id', '!=', False),
                ('partner_id.credit_limit', '>', 0)
            ]
        )
        if address_ids:
            _logger.info('Total=%s' % len(address_ids))
            for address_id in address_ids:
                _logger.info('Enviando SNS %s' % address_id.id)
                address_id.action_credit_limit_send_sns()
                
    @api.multi
    def action_credit_limit_send_sns_multi(self):
        for item in self:
            _logger.info('Enviando SNS %s' % item.id)
            item.action_credit_limit_send_sns()

    @api.multi
    def action_credit_limit_send_sns(self):
        self.ensure_one()
        _logger.info('action_credit_limit_send_sns')
        if self.partner_id.credit_limit > 0:
            action_response = True
            # define
            ses_sqs_url = tools.config.get('ses_sqs_url')
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
                'credit_limit': self.partner_id.credit_limit,
                'max_credit_limit_allow':
                    self.partner_id.max_credit_limit_allow,
                'cesce_risk_state': str(self.partner_id.cesce_risk_state)
            }
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
            response = sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:534422648921:'+str(sns_name),
                Message=json.dumps(message, indent=2),
                MessageAttributes={
                    'Headers': {
                        'DataType': 'String',
                        'StringValue': json.dumps([{'type': 'Oniad\\Domain\\Odoo\\OdooCreditAvailableEvent'},[]])
                    }
                }                                
            )
            if 'MessageId' not in response:
                action_response = False
            else:
                _logger.info(sns_name)                        
            # return
            return action_response
