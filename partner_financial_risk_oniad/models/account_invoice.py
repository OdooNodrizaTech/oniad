# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    invoice_with_risk = fields.Boolean(
        string='Invoice With Risk' 
    )
    
    @api.multi
    def action_invoice_open(self):
        return_object = super(AccountInvoice, self).action_invoice_open()
        #partner_id credit_limit
        if self.partner_id.credit_limit>0:
            self.invoice_with_risk = True
        else:
            self.invoice_with_risk = False            
        #return                            
        return return_object                    