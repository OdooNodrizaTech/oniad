# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'
            
    sale_user_id = fields.Many2one(
        comodel_name='res.users',        
        string='Usuario venta'
    )
    oniad_contact_use = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('communications','Comuniaciones')                          
        ],
        default='none',
        string='Uso Contacto (OniAd)'
    )    
    
    @api.one
    def write(self, vals):
        allow_write = True
        #check_dni
        if self.type=='contact' and self.parent_id.id==0:
            if 'vat' in vals:
                if vals['vat']!=False:       
                    vals['vat'] = vals['vat'].strip().replace(' ', '').upper()#force to uppercase and remove spaces
                
                    if self.country_id.id > 0 and self.country_id.code=='ES':
                        if '-' in vals['vat']:
                            allow_write = False
                            raise Warning("El NIF no permite el caracter '-'")
                                                    
        if allow_write==True:                        
            return_write = super(ResPartner, self).write(vals)        