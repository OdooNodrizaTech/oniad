# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerFanLevel(models.Model):
    _name = 'res.partner.fan.level'

    name = fields.Char(
        string="Nombre"
    )     