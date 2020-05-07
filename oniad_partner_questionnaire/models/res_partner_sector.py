# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerSector(models.Model):
    _name = 'res.partner.sector'
    _description = 'Res Partner Sector'

    name = fields.Char(
        string="Nombre"
    )     