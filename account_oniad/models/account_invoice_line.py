# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    purchase_price = fields.Monetary(         
        string='Purchase price'
    )
    
    @api.model
    def create(self, values):
        res = super(AccountInvoiceLine, self).create(values)
        # purchase_price
        if res.purchase_price == 0:
            purchase_line = 0
            for line_id in res.sale_line_ids:
                if line_id:
                    purchase_line = purchase_line + line_id.purchase_price
            
            res.purchase_price = purchase_line
        # return
        return res
