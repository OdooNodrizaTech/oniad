# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, vals):
        # need_send_sns
        if 'credit_limit' in vals:
            credit_limit_old = self.credit_limit
        # super
        res = super(ResPartner, self).write(vals)
        # need_send_sns
        if 'credit_limit' in vals:
            if res.credit_limit != credit_limit_old:
                if res.oniad_address_id:
                    res.oniad_address_id.action_credit_limit_send_sns()
        # return
        return res
