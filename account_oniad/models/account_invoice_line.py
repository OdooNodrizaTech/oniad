# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
import uuid

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    purchase_price = fields.Monetary(         
        string='Coste'
    )
    
    @api.model
    def create(self, values):
        return_object = super(AccountInvoiceLine, self).create(values)
        
        if return_object.purchase_price==0:
            purchase_price_sale_line = 0
            for sale_line_id in return_object.sale_line_ids:
                if sale_line_id.id>0:
                    purchase_price_sale_line = purchase_price_sale_line + sale_line_id.purchase_price  
            
            return_object.purchase_price = purchase_price_sale_line                                        
                            
        return return_object                    