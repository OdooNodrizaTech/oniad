# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools
import json

import logging
_logger = logging.getLogger(__name__)

class OniadAddress(models.Model):
    _inherit = 'oniad.address'
    
    @api.model
    def check_vat_error(self, vat, id):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        slack_log_channel = self.env['ir.config_parameter'].sudo().get_param('slack_log_channel')
        
        attachments = [
            {                    
                "title": 'El VAT es incorrecto',
                "text": vat,                        
                "color": "#ff0000",                                             
                "fallback": "Ver oniad address "+str(web_base_url)+"/web?#id="+str(id)+"&view_type=form&model=oniad.address",                                    
                "actions": [
                    {
                        "type": "button",
                        "text": "Ver registro",
                        "url": str(web_base_url)+"/web?#id="+str(id)+"&view_type=form&model=oniad.address"
                    }
                ],
                "fields": [                    
                    {
                        "title": "VAT",
                        "value": vat,
                        'short': True,
                    },
                    {
                        "title": "Id",
                        "value": id,
                        'short': True,
                    }
                ],                    
            }
        ]        
        slack_message_vals = {                        
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': slack_log_channel,                                                         
        }                        
        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)