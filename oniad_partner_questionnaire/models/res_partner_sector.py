# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerSector(models.Model):
    _name = 'res.partner.sector'

    name = fields.Char(
        string="Nombre"
    )     