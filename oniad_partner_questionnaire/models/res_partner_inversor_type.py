# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerInversorType(models.Model):
    _name = 'res.partner.inversor.type'
    _description = 'Res Partner Inversor Type'

    name = fields.Char(
        string="Nombre"
    )     