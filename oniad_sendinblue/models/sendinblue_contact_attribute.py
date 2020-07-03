# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

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