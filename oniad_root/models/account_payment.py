# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User'
    )
    oniad_transaction_id = fields.Many2one(
        comodel_name='oniad.transaction',
        string='Oniad Transaction'
    )
