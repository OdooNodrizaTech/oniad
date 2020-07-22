# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, tools


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
                "fallback": "Ver oniad address %s/web?#id=%s&view_type=form&model=oniad.address" % (web_base_url, id),
                "actions": [
                    {
                        "type": "button",
                        "text": "Ver registro",
                        "url": "%s/web?#id=%s&view_type=form&model=oniad.address" % (web_base_url, id)
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
        vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'as_user': True,
            'channel': slack_log_channel,                                                         
        }                        
        self.env['slack.message'].sudo().create(vals)