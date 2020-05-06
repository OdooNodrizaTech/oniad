# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerEducationalCenterType(models.Model):
    _name = 'res.partner.educational.center.type'

    name = fields.Char(
        string="Nombre"
    )     