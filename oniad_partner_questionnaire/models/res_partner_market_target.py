# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerMarketTarget(models.Model):
    _name = 'res.partner.market.target'

    name = fields.Char(
        string="Nombre"
    )     