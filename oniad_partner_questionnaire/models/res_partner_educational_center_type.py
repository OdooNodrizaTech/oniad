# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerEducationalCenterType(models.Model):
    _name = 'res.partner.educational.center.type'
    _description = 'Res Partner Educational Center Type'

    name = fields.Char(
        string="Nombre"
    )     