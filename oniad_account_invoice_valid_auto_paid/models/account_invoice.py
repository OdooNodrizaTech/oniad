# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'                     
    
    @api.multi
    def action_invoice_open(self):
        #action
        return_action = super(AccountInvoice, self).action_invoice_open()
        #operations
        for obj in self:
            if obj.amount_total!=0:
                if obj.type in ['out_invoice', 'out_refund']:
                    oniad_transaction_ids = []
                    for invoice_line_id in obj.invoice_line_ids:
                        if invoice_line_id.oniad_transaction_id.id>0:
                            if invoice_line_id.oniad_transaction_id.id not in oniad_transaction_ids:
                                oniad_transaction_ids.append(int(invoice_line_id.oniad_transaction_id.id))                        
                    #check
                    if len(oniad_transaction_ids)>0:                        
                        oniad_transaction_ids = self.env['oniad.transaction'].sudo().search(
                            [
                                ('id', 'in', oniad_transaction_ids),
                                ('account_payment_id', '!=', False)
                            ]
                        )
                        if len(oniad_transaction_ids)>0:
                            for oniad_transaction_id in oniad_transaction_ids:
                                if oniad_transaction_id.account_payment_id.payment_type=='inbound':
                                    for move_line_id in oniad_transaction_id.account_payment_id.move_line_ids:                        
                                        if move_line_id.credit>0:
                                            _logger.info('Factura '+str(obj.id)+' pre-asignar asiento contable '+str(move_line_id.id)+ ' del pago '+str(oniad_transaction_id.account_payment_id.id))
                                            obj.assign_outstanding_credit(move_line_id.id)
                                            _logger.info('Factura '+str(obj.id)+' asignado asiento contable '+str(move_line_id.id)+ ' del pago '+str(oniad_transaction_id.account_payment_id.id))
                                elif oniad_transaction_id.account_payment_id.payment_type=='outbound':
                                    for move_line_id in oniad_transaction_id.account_payment_id.move_line_ids:
                                        if move_line_id.debit>0:
                                            _logger.info('Factura '+str(obj.id)+' pre-asignar asiento contable '+str(move_line_id.id)+ ' del pago '+str(oniad_transaction_id.account_payment_id.id))
                                            obj.assign_outstanding_credit(move_line_id.id)
                                            _logger.info('Factura '+str(obj.id)+' asignado asiento contable '+str(move_line_id.id)+ ' del pago '+str(oniad_transaction_id.account_payment_id.id))                                    
        #return
        return return_action        