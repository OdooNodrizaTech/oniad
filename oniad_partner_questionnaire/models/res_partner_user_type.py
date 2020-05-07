# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerUserType(models.Model):
    _name = 'res.partner.user.type'
    _description = 'res.partner.user.type'

    name = fields.Char(
        string="Nombre"
    )     