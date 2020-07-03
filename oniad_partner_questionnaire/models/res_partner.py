# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ResPartnerCustom(models.Model):
    _inherit = 'res.partner'
    
    oa_qt_partner_type = fields.Many2many(
        comodel_name='res.partner.partner.type',         
        string='Tipo de contacto',
    ) 
    
    @api.onchange('oa_qt_partner_type')
    def change_oa_qt_partner_type(self):
       self._get_oa_qt_show_stakeholder_tab()
       self._get_oa_qt_show_user_tab()
    #calculate field show_stakeholdert_tab       
    oa_qt_show_stakeholder_tab = fields.Boolean(
        compute='_get_oa_qt_show_stakeholder_tab',
        store=False
    )    
    @api.one        
    def _get_oa_qt_show_stakeholder_tab(self):
        for partner_obj in self:          
            partner_obj.oa_qt_show_stakeholder_tab = False            
            for item in partner_obj.oa_qt_partner_type:            
                if item.stakeholder==True:
                    partner_obj.oa_qt_show_stakeholder_tab = True
                         
    #calculate field user tab
    oa_qt_show_user_tab = fields.Boolean(
        compute='_get_oa_qt_show_user_tab',
        store=False
    )    
    @api.one        
    def _get_oa_qt_show_user_tab(self):
        for partner_obj in self:          
            partner_obj.oa_qt_show_user_tab = False            
            for item in partner_obj.oa_qt_partner_type:            
                if item.user==True:
                    partner_obj.oa_qt_show_user_tab = True
            
    oa_qt_stakeholder_type = fields.Many2many(
        comodel_name='res.partner.stakeholder.type',         
        string='Tipo de Stakeholder',
    )
    
    @api.onchange('oa_qt_stakeholder_type')
    def change_oa_qt_stakeholder_type(self):
       self._get_oa_qt_is_fan()
       self._get_oa_qt_is_investor()
       self._get_oa_qt_is_teacher()
       self._get_oa_qt_is_association()
       self._get_oa_qt_is_communicator()
       self._get_oa_qt_is_communicator_influencer()#fix
       
    #calculate field oa_qt_is_fan       
    oa_qt_is_fan = fields.Boolean(
        compute='_get_oa_qt_is_fan',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_fan(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_fan = False            
            for item in partner_obj.oa_qt_stakeholder_type:            
                if item.fan==True:
                    partner_obj.oa_qt_is_fan = True
                                                                            
    #calculate field oa_qt_is_investor       
    oa_qt_is_investor = fields.Boolean(
        compute='_get_oa_qt_is_investor',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_investor(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_investor = False            
            for item in partner_obj.oa_qt_stakeholder_type:            
                if item.investor==True:
                    partner_obj.oa_qt_is_investor = True
                        
    #calculate field oa_qt_is_teacher       
    oa_qt_is_teacher = fields.Boolean(
        compute='_get_oa_qt_is_teacher',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_teacher(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_teacher = False            
            for item in partner_obj.oa_qt_stakeholder_type:            
                if item.teacher==True:
                    partner_obj.oa_qt_is_teacher = True
                    
    #calculate field oa_qt_is_association       
    oa_qt_is_association = fields.Boolean(
        compute='_get_oa_qt_is_association',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_association(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_association = False            
            for item in partner_obj.oa_qt_stakeholder_type:            
                if item.association==True:
                    partner_obj.oa_qt_is_association = True
    
    #calculate field oa_qt_is_communicator       
    oa_qt_is_communicator = fields.Boolean(
        compute='_get_oa_qt_is_communicator',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_communicator(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_communicator = False            
            for item in partner_obj.oa_qt_stakeholder_type:            
                if item.communicator==True:
                    partner_obj.oa_qt_is_communicator = True
    
    oa_qt_fan_level = fields.Many2many(
        comodel_name='res.partner.fan.level',         
        string='Nivel de fan',
    )
    oa_qt_inversor_type = fields.Many2many(
        comodel_name='res.partner.inversor.type',         
        string='Tipo de inversor',
    )
    oa_qt_educational_center_type = fields.Many2many(
        comodel_name='res.partner.educational.center.type',         
        string='Tipo de centro educativo',
    )
    oa_qt_formation_type = fields.Many2many(
        comodel_name='res.partner.formation.type',         
        string='Tipo de formation',
    )
    oa_qt_asociation_type = fields.Many2many(
        comodel_name='res.partner.asociation.type',         
        string='Tipo de asociacion',
    )
    oa_qt_asociation_geo = fields.Many2many(
        comodel_name='res.partner.asociation.geo',         
        string='Geo de asociacion',
    )
    oa_qt_communicator_type = fields.Many2many(
        comodel_name='res.partner.communicator.type',         
        string='Tipo de comunicador',
    )
    @api.onchange('oa_qt_communicator_type')
    def change_oa_qt_communicator_type(self):       
       self._get_oa_qt_is_communicator_influencer()#fix
    
    #calculate field oa_qt_is_communicator_influencer       
    oa_qt_is_communicator_influencer = fields.Boolean(
        compute='_get_oa_qt_is_communicator_influencer',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_communicator_influencer(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_communicator_influencer = False            
            for item in partner_obj.oa_qt_communicator_type:            
                if item.influencer==True:
                    partner_obj.oa_qt_is_communicator_influencer = True
    
    oa_qt_social_network = fields.Many2many(
        comodel_name='res.partner.social.network',         
        string='Red social',
    )
    oa_qt_communication_area = fields.Many2many(
        comodel_name='res.partner.communication.area',         
        string='Ambito de comunicacion',
    )
    oa_qt_communication_geo = fields.Many2many(
        comodel_name='res.partner.communication.geo',         
        string='Geo de comunicacion',
    )    
    
    
    oa_qt_user_type = fields.Many2one(
        comodel_name='res.partner.user.type',         
        string='Tipo de Usuario',
    )
    oa_qt_customer_type = fields.Many2one(
        comodel_name='res.partner.customer.type',         
        string='Tipo de Cliente',
    )
    
    @api.onchange('oa_qt_customer_type')
    def change_oa_qt_customer_type(self):
       self._get_oa_qt_is_advertiser()
       self._get_oa_qt_is_agency()
        
    #calculate field oa_qt_is_agency       
    oa_qt_is_agency = fields.Boolean(
        compute='_get_oa_qt_is_agency',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_agency(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_agency = False            
            for item in partner_obj.oa_qt_customer_type:            
                if item.agency==True:
                    partner_obj.oa_qt_is_agency = True
    
    oa_qt_agency_type = fields.Many2many(
        comodel_name='res.partner.agency.type',         
        string='Tipo de agencia',
    )    
    #calculate field oa_qt_is_advertiser       
    oa_qt_is_advertiser = fields.Boolean(
        compute='_get_oa_qt_is_advertiser',
        store=False
    )    
    @api.one        
    def _get_oa_qt_is_advertiser(self):
        for partner_obj in self:          
            partner_obj.oa_qt_is_advertiser = False            
            for item in partner_obj.oa_qt_customer_type:            
                if item.advertiser==True:
                    partner_obj.oa_qt_is_advertiser = True        
    
    oa_qt_affiliate = fields.Boolean(
        string="Afiliado"
    )
    oa_qt_market_target = fields.Many2many(
        comodel_name='res.partner.market.target',         
        string='Mercado objetivo',
    )
    oa_qt_sector = fields.Many2one(
        comodel_name='res.partner.sector',         
        string='Sector',
    )
    oa_qt_activity = fields.Many2many(
        comodel_name='res.partner.activity',         
        string='Actividad',
    )
    oa_qt_agency_activity = fields.Many2many(
        comodel_name='res.partner.agency.activity',         
        string='Actividad de agencia',
    )                                         