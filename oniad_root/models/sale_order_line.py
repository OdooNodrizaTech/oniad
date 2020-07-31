# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
        
    oniad_transaction_id = fields.Many2one(
        comodel_name='oniad.transaction',
        string='Oniad Transaction'
    )
    
    @api.model
    def create(self, values):
        res = super(SaleOrderLine, self).create(values)
        # Fix
        if res.oniad_transaction_id:
            res.product_id_change()
            # update
            res.price_tax = res.oniad_transaction_id.tax
            res.price_unit = res.oniad_transaction_id.amount
            res.price_subtotal = res.oniad_transaction_id.total
        # return
        return res
