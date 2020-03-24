# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class SendinblueEnumeration(models.Model):
    _name = 'sendinblue.enumeration'    
            
    label = fields.Char(        
        string='Etiqueta'
    )
    value = fields.Integer(        
        string='Valor'
    )               