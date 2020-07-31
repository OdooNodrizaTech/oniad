# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        compute='_compute_oniad_address_id',
        string='Oniad Address',
        store=True
    )
    oniad_transaction_count = fields.Integer(
        compute='_compute_oniad_transaction_count',
        string="Oniad Transactions",
    )

    @api.multi
    def _compute_oniad_transaction_count(self):
        for item in self:
            item.oniad_transaction_count = len(
                self.env['oniad.transaction'].search(
                    [
                        ('sale_order_id', '=', item.id)
                    ]
                )
            )

    @api.depends('partner_invoice_id.oniad_address_id')
    def _compute_oniad_address_id(self):
        for item in self:
            if item.id:
                if item.partner_invoice_id.oniad_address_id:
                    item.oniad_address_id = item.partner_invoice_id.oniad_address_id.id
