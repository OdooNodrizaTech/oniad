# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SendinblueEnumeration(models.Model):
    _name = 'sendinblue.enumeration'
    _description = 'Sendinblue Enumeration'    
            
    label = fields.Char(        
        string='Etiqueta'
    )
    value = fields.Integer(        
        string='Valor'
    )               