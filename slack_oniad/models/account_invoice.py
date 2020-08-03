# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_auto_create_message_slack(self):
        self.ensure_one()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url_item = "%s/web?#id=%s&view_type=form&model=account.invoice" % (
            web_base_url,
            self.id
        )
        attachments = [
            {
                "title": _('Se ha creado la factura de OniAd automaticamente'),
                "text": self.number,
                "fallback": "Ver factura %s" % url_item,
                "color": "#36a64f",
                "actions": [
                    {
                        "type": "button",
                        "text": _("Ver factura"),
                        "url": url_item
                    }
                ],
                "fields": [
                    {
                        "title": _("Cliente"),
                        "value": self.partner_id.name,
                        'short': True,
                    },
                    {
                        "title": _("Importe"),
                        "value": "%s %s" % (
                            self.amount_total,
                            self.currency_id.symbol
                        ),
                        'short': True,
                    }
                ],
            }
        ]
        vals = {
            'attachments': attachments,
            'model': 'account.invoice',
            'res_id': self.id,
            'channel': self.env['ir.config_parameter'].sudo().get_param(
                'slack_log_contabilidad_channel'
            ),
        }
        self.env['slack.message'].sudo().create(vals)
