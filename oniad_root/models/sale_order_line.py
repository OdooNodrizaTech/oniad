# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
        
    oniad_transaction_id = fields.Many2one(
        comodel_name='oniad.transaction',
        string='Oniad Transaction'
    )
    
    @api.model
    def create(self, values):
        return_object = super(SaleOrderLine, self).create(values)
        #Fix
        if return_object.oniad_transaction_id.id>0:
            return_object.product_id_change()
            #update            
            return_object.price_tax = return_object.oniad_transaction_id.tax
            return_object.price_unit = return_object.oniad_transaction_id.amount
            return_object.price_subtotal = return_object.oniad_transaction_id.total                                                                                                                    
        #return                            
        return return_object