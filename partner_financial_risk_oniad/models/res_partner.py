# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.one
    def write(self, vals):
        #need_send_sns
        if 'credit_limit' in vals:
            credit_limit_old = self.credit_limit
        #super                                                               
        return_object = super(ResPartner, self).write(vals)
        #need_send_sns
        if 'credit_limit' in vals:
            if self.credit_limit!=credit_limit_old:
                if self.oniad_address_id.id>0:
                    #Como ha cambiado el credit_limit, enviamos el SNS
                    self.oniad_address_id.action_credit_limit_send_sns()
        #return
        return return_object