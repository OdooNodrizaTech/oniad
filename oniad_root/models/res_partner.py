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