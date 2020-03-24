# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'            
    
    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
            
        if self.partner_id.vat==False:
            allow_action_confirm = False
            raise Warning("Es necesario definir VAT para el cliente antes de validar el pedido de venta.\n")                                                                                                     
        else:
            if self.need_check_credit_limit==True:
                future_max_credit_limit_allow = self.max_credit_limit_allow - self.amount_total
                if future_max_credit_limit_allow<=0:
                    allow_action_confirm = False
                    raise Warning("No se puede confirmar la venta porque no hay credito disponible o el importe total de esta venta es superior al credito disponible ("+str(future_max_credit_limit_allow)+")")
            
        if allow_action_confirm==True:
            return super(SaleOrder, self).action_confirm()