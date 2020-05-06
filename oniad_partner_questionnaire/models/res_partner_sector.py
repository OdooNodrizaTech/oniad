# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerSector(models.Model):
    _name = 'res.partner.sector'

    name = fields.Char(
        string="Nombre"
    )     