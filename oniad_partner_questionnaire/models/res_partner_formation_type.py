# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerFormationType(models.Model):
    _name = 'res.partner.formation.type'
    _description = 'Res Partner Formation Type'

    name = fields.Char(
        string="Nombre"
    )     