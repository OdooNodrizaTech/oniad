# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        string='Oniad Address'
    )          
        
    @api.multi
    def compute_taxes(self):
        return_object = super(AccountInvoice, self).compute_taxes()
        #update
        for obj in self:
            oniad_transaction_ids = []
            for invoice_line_id in obj.invoice_line_ids:
                if invoice_line_id.oniad_transaction_id.id>0:
                    oniad_transaction_ids.append(invoice_line_id.oniad_transaction_id.id)
            #Fix tax_line_ids
            if len(oniad_transaction_ids)>0:
                #calculate
                tax_amount = 0
                tax_base = 0
                oniad_transaction_ids = self.env['oniad.transaction'].sudo().search([('id', 'in', oniad_transaction_ids)])
                if len(oniad_transaction_ids)>0:
                    for oniad_transaction_id in oniad_transaction_ids:
                        tax_amount += oniad_transaction_id.tax
                        tax_base += oniad_transaction_id.amount
                #update                            
                if len(obj.tax_line_ids)>0:
                    obj.tax_line_ids[0].amount = tax_amount
                    obj.tax_line_ids[0].base = tax_base
        #return
        return return_object    