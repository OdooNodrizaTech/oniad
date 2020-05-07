# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerSocialNetwork(models.Model):
    _name = 'res.partner.social.network'
    _description = 'Res Partner Social Network'

    name = fields.Char(
        string="Nombre"
    )     