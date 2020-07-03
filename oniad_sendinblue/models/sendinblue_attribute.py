# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from ..sendinblue.web_service import SendinblueWebService

class SendinblueAttribute(models.Model):
    _name = 'sendinblue.attribute'
    _description = 'Sendinblue Attribute'    
        
    name = fields.Char(        
        string='Nombre'
    )
    category = fields.Char(        
        string='Categoria'
    )
    sendinblue_type = fields.Char(        
        string='Tipo'
    )
    sendinblue_enumeration_ids = fields.Many2many(
        comodel_name='sendinblue.enumeration',
        string='Valores'
    )
    calculated_value = fields.Char(        
        string='Valor calculado'
    )    
    
    @api.model    
    def cron_get_attributes(self):
        sendinblue_web_service = SendinblueWebService(self.env.user.company_id, self.env)
        return_get_attributes = sendinblue_web_service.get_attributes()
        if return_get_attributes['errors']==False:
            if len(return_get_attributes['response'].attributes)>0:
                #fix enumeration
                for attribute in return_get_attributes['response'].attributes:
                    if attribute.enumeration!=None:                            
                        for enumeration_item in attribute.enumeration:   
                            sendinblue_enumeration_ids = self.env['sendinblue.enumeration'].search([('label', '=', enumeration_item.label),('value', '=', enumeration_item.value)])
                            if len(sendinblue_enumeration_ids)==0:
                                sendinblue_enumeration_vals = {                                        
                                    'label': enumeration_item.label,
                                    'value': enumeration_item.value,                                                                                                                 
                                }                        
                                sendinblue_enumeration_obj = self.env['sendinblue.enumeration'].sudo().create(sendinblue_enumeration_vals)
                #attributes
                for attribute in return_get_attributes['response'].attributes:                                                
                    #attribute
                    sendinblue_attribute_ids = self.env['sendinblue.attribute'].search([('name', '=', attribute.name)])
                    if len(sendinblue_attribute_ids)>0:
                        sendinblue_attribute_obj = sendinblue_attribute_ids[0]                        
                        #sendinblue_enumeration_ids
                        sendinblue_enumeration_ids = []
                        if attribute.enumeration!=None:                            
                            for enumeration_item in attribute.enumeration:   
                                sendinblue_enumeration_ids_get = self.env['sendinblue.enumeration'].search([('label', '=', enumeration_item.label),('value', '=', enumeration_item.value)])                                
                                if len(sendinblue_enumeration_ids_get)>0:
                                    sendinblue_enumeration_id_get = sendinblue_enumeration_ids_get[0]
                                    sendinblue_enumeration_ids.append(sendinblue_enumeration_id_get.id)                                                           
                        
                        sendinblue_attribute_obj.update({
                            'name': attribute.name,
                            'category': attribute.category,
                            'sendinblue_type': attribute.type,
                            'calculated_value': attribute.calculated_value,
                            'sendinblue_enumeration_ids': sendinblue_enumeration_ids,
                        })                                                                                                                                                                                                                                        
                    else:
                        sendinblue_attribute_vals = {                                
                            'name': attribute.name,
                            'category': attribute.category,
                            'sendinblue_type': attribute.type,
                            'calculated_value': attribute.calculated_value,                                                                                                                 
                        }                        
                        sendinblue_attribute_obj = self.env['sendinblue.attribute'].sudo().create(sendinblue_attribute_vals)                        