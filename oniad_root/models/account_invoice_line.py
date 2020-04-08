# -*- coding: utf-8 -*-
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
        #return                            
        return return_object