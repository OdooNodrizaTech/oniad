# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User'
    )
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        string='Oniad Address'
    )
    oniad_user_id_link = fields.Char(
        compute='_oniad_user_id_link',
        string='OniAd User',
        store=False
    )
    
    @api.multi        
    def _oniad_user_id_link(self):
        for record in self:
            if record.id>0:
                if record.oniad_user_id.id>0: 
                    record.oniad_user_id_link = 'https://platform.oniad.com/backend/admin/supadmin/card/'+str(record.oniad_user_id.id)

    @api.model
    def check_vat_custom(self, vat=None):
        if self.env.context.get('company_id'):
            company = self.env['res.company'].browse(self.env.context['company_id'])
        else:
            company = self.env.user.company_id
        if company.vat_check_vies:
            # force full VIES online check
            check_func = self.vies_vat_check
        else:
            # quick and partial off-line checksum validation
            check_func = self.simple_vat_check
            
        if vat==None:
            return False
        
        vat_country, vat_number = self._split_vat(vat)
        if check_func(vat_country, vat_number):
            return True
        else:
            _logger.info("Importing VAT Number [%s] is not valid !" % vat_number)
            return False
            
    @api.one
    def write(self, vals):
        send_sns_oniad_address_id_custom = False        
        #customer_payment_mode_id
        if 'customer_payment_mode_id' in vals:
            customer_payment_mode_id_old = self.customer_payment_mode_id.id
        #property_payment_term_id            
        if 'property_payment_term_id' in vals:
            property_payment_term_id_old = self.property_payment_term_id.id            
        #super                                                               
        return_object = super(ResPartner, self).write(vals)
        #customer_payment_mode_id
        if 'customer_payment_mode_id' in vals:
            if self.customer_payment_mode_id.id!=customer_payment_mode_id_old:
                send_sns_oniad_address_id_custom = True
        #property_payment_term_id
        if 'property_payment_term_id' in vals:
            if self.property_payment_term_id.id!=property_payment_term_id_old:
                send_sns_oniad_address_id_custom = True                
        #send
        if send_sns_oniad_address_id_custom==True:
            if self.oniad_address_id.id>0:
                #Como ha cambiado el customer_payment_mode_id o property_payment_term_id enviamos
                self.oniad_address_id.action_send_sns()
        #return
        return return_object                                                                 