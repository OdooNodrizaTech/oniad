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
    
    @api.one        
    def oniad_root_complete_data(self, product, account_payment_ids):
        #account.invoice.lines
        payments_total = 0                        
        for account_payment_id in account_payment_ids:
            #account_invoice_line_vals
            account_invoice_line_vals = {
                'invoice_id': self.id,
                'oniad_transaction_id': account_payment_id.oniad_transaction_id.id,
                'product_id': product.id,#Producto Gasto
                'name': account_payment_id.communication,
                'quantity': 1,
                'price_unit': account_payment_id.amount,
                'account_id': product.property_account_income_id.id,
                'purchase_price': account_payment_id.oniad_purchase_price,
                'currency_id': account_payment_id.currency_id.id                     
            }
            #oniad_product_id
            if account_payment_id.oniad_product_id.id>0:
                account_invoice_line_vals['product_id'] = account_payment_id.oniad_product_id.id 
            #create
            account_invoice_line_obj = self.env['account.invoice.line'].sudo().create(account_invoice_line_vals)
            account_invoice_line_obj._onchange_product_id()
            account_invoice_line_obj._onchange_account_id()                
            #price
            price_unit = account_payment_id.amount/((account_invoice_line_obj.invoice_line_tax_ids.amount/100)+1)            
            payments_total = payments_total + account_payment_id.amount
            #update
            account_invoice_line_obj.update({
                'price_unit': round(price_unit,4),
                'name': account_payment_id.communication,
                'price_subtotal': price_unit,
            })
        #Fix check totals
        self.compute_taxes()
        #check
        if payments_total>self.amount_total:
            amount_rest = payments_total-self.amount_total
            for tax_line_id in self.tax_line_ids:
                tax_line_id.amount = tax_line_id.amount + amount_rest
            #update tax_line_ids
            self.update({'tax_line_ids': self.tax_line_ids})
        elif self.amount_total>payments_total:
            amount_rest = self.amount_total-payments_total
            for tax_line_id in self.tax_line_ids:
                tax_line_id.amount = tax_line_id.amount - amount_rest
            #update tax_line_ids
            self.update({'tax_line_ids': self.tax_line_ids})
        #update payment.invoice            
        _logger.info('Factura '+str(self.id)+' actualizada correctamente')
        #operations
        if self.partner_id.vat!=False and self.partner_id.vat!="":
            self.action_invoice_open()
            _logger.info('Factura '+str(self.id)+' validada correctamente')                
            self.action_auto_create_message_slack()#slack.message                                
            #payments
            if len(account_payment_ids)>0:
                for account_payment_id in account_payment_ids:
                    if account_payment_id.payment_type=='inbound':
                        for move_line_id in account_payment_id.move_line_ids:                        
                            if move_line_id.credit>0:
                                _logger.info('Factura '+str(self.id)+' pre-asignar asiento contable '+str(move_line_id.id)+ ' del pago '+str(account_payment_id.id))
                                self.assign_outstanding_credit(move_line_id.id)
                                _logger.info('Factura '+str(self.id)+' asignado asiento contable '+str(move_line_id.id)+ ' del pago '+str(account_payment_id.id))
                    elif account_payment_id.payment_type=='outbound':
                        for move_line_id in account_payment_id.move_line_ids:
                            if move_line_id.debit>0:
                                _logger.info('Factura '+str(self.id)+' pre-asignar asiento contable '+str(move_line_id.id)+ ' del pago '+str(account_payment_id.id))
                                self.assign_outstanding_credit(move_line_id.id)
                                _logger.info('Factura '+str(self.id)+' asignado asiento contable '+str(move_line_id.id)+ ' del pago '+str(account_payment_id.id))