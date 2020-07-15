# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
        
    oniad_transaction_id = fields.Many2one(
        comodel_name='oniad.transaction',
        string='Oniad Transaction'
    )
    
    @api.model
    def create(self, values):
        return_object = super(AccountInvoiceLine, self).create(values)
        #sale_line_ids (oniad_transaction_id)
        for sale_line_id in return_object.sale_line_ids:
            if sale_line_id.oniad_transaction_id.id>0:
                return_object.oniad_transaction_id = sale_line_id.oniad_transaction_id.id
        #Fix
        if return_object.oniad_transaction_id.id>0:
            return_object._onchange_product_id()
            return_object._onchange_account_id()
            # Fix account_invoice_id in oniad_transaction_id
            return_object.oniad_transaction_id.account_invoice_id = return_object.invoice_id.id
            #update
            return_object.price_unit = return_object.oniad_transaction_id.amount
            return_object.price_subtotal = return_object.oniad_transaction_id.total                                                                                            
        #return                            
        return return_object