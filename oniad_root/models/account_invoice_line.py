# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
        
    oniad_transaction_id = fields.Many2one(
        comodel_name='oniad.transaction',
        string='Oniad Transaction'
    )
    
    @api.model
    def create(self, values):
        res = super(AccountInvoiceLine, self).create(values)
        # sale_line_ids (oniad_transaction_id)
        for line_id in res.sale_line_ids:
            if line_id.oniad_transaction_id:
                res.oniad_transaction_id = line_id.oniad_transaction_id.id
        # Fix
        if res.oniad_transaction_id:
            res._onchange_product_id()
            res._onchange_account_id()
            # Fix account_invoice_id in oniad_transaction_id
            res.oniad_transaction_id.account_invoice_id = res.invoice_id.id
            # update
            res.price_unit = res.oniad_transaction_id.amount
            res.price_subtotal = res.oniad_transaction_id.total
        # return
        return res
