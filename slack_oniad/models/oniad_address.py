# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, _


class OniadAddress(models.Model):
    _inherit = 'oniad.address'

    @api.model
    def check_vat_error(self, vat, id):
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        slack_log_channel = self.env['ir.config_parameter'].sudo().get_param(
            'slack_log_channel'
        )
        item_url = "%s/web?#id=%s&view_type=form&model=oniad.address" % (
            web_base_url,
            id
        )
        attachments = [
            {
                "title": _('El VAT es incorrecto'),
                "text": vat,
                "color": "#ff0000",
                "fallback": _("Ver oniad address %s") % item_url,
                "actions": [
                    {
                        "type": "button",
                        "text": _("Ver registro"),
                        "url": item_url
                    }
                ],
                "fields": [
                    {
                        "title": _("VAT"),
                        "value": vat,
                        'short': True,
                    },
                    {
                        "title": _("Id"),
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
