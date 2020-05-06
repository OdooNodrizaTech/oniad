# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SendinblueContactAttribute(models.Model):
    _name = 'sendinblue.contact.attribute'    
    
    sendinblue_contact_id = fields.Many2one(
        comodel_name='sendinblue.contact',
        string='Sendinblue Contacto'
    )
    sendinblue_attribute_id = fields.Many2one(
        comodel_name='sendinblue.attribute',
        string='Sendinblue Atributos'
    )
    sendinblue_enumeration_id = fields.Many2one(
        comodel_name='sendinblue.enumeration',
        string='Sendinblue Enumeration'
    )
    value = fields.Char(        
        string='Valor'
    )    