# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerFormationType(models.Model):
    _name = 'res.partner.formation.type'

    name = fields.Char(
        string="Nombre"
    )     