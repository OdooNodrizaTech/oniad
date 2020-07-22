# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    oniad_product_id = fields.Many2one(
        comodel_name='product.template',         
        string='OniAd Product'
    )
    oniad_purchase_price = fields.Monetary(         
        string='OniAd Purchase price'
    )