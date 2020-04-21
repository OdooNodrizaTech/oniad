# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        compute='_oniad_user_id',
        string='Oniad User',
        store=False
    )
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        compute='_oniad_address_id',
        string='Oniad Address',
        store=False
    )
    
    @api.multi        
    def _oniad_user_id(self):
        for record in self:
            if record.id>0:
                oniad_user_ids = self.env['oniad.user'].search([('partner_id', '=', record.id)])
                if len(oniad_user_ids)>0:
                    record.oniad_user_id = oniad_user_ids[0].id
                    
    @api.multi        
    def _oniad_address_id(self):
        for record in self:
            if record.id>0:
                oniad_address_ids = self.env['oniad.address'].search([('partner_id', '=', record.id)])
                if len(oniad_address_ids)>0:
                    record.oniad_address_id = oniad_address_ids[0].id                                                     
    
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