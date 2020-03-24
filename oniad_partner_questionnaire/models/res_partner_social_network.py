# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerSocialNetwork(models.Model):
    _name = 'res.partner.social.network'

    name = fields.Char(
        string="Nombre"
    )     