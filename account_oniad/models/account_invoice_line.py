# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    purchase_price = fields.Monetary(         
        string='Purchase price'
    )
    
    @api.model
    def create(self, values):
        return_object = super(AccountInvoiceLine, self).create(values)
        # purchase_price
        if return_object.purchase_price == 0:
            purchase_price_sale_line = 0
            for sale_line_id in return_object.sale_line_ids:
                if sale_line_id:
                    purchase_price_sale_line = purchase_price_sale_line + sale_line_id.purchase_price  
            
            return_object.purchase_price = purchase_price_sale_line                                        
        # return
        return return_object                    