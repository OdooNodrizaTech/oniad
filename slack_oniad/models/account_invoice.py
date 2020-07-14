# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one    
    def action_auto_create_message_slack(self):        
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                                                                        
        attachments = [
            {
                "title": 'Se ha creado la factura de OniAd automaticamente',
                "text": self.number,
                "fallback": "Ver factura "+str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=account.invoice",
                "color": "#36a64f",
                "actions": [
                    {
                        "type": "button",
                        "text": "Ver factura",
                        "url": str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=account.invoice"
                    }
                ],
                "fields": [                    
                    {
                        "title": "Cliente",
                        "value": self.partner_id.name,
                        'short': True,
                    },
                    {
                        "title": "Importe",
                        "value": str(self.amount_total)+' '+self.currency_id.symbol,
                        'short': True,
                    }
                ],
            }
        ]        
        slack_message_vals = {
            'attachments': attachments,
            'model': 'account.invoice',
            'res_id': self.id,
            'channel': self.env['ir.config_parameter'].sudo().get_param('slack_log_contabilidad_channel'),                                                         
        }                        
        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)