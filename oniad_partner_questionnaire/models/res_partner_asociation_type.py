# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerAsociationType(models.Model):
    _name = 'res.partner.asociation.type'

    name = fields.Char(
        string="Nombre"
    )     