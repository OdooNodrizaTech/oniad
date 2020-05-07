# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerMarketTarget(models.Model):
    _name = 'res.partner.market.target'
    _description = 'Res Partner Market Target'

    name = fields.Char(
        string="Nombre"
    )     