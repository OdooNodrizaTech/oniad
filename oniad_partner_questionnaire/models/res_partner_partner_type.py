# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerPartnerType(models.Model):
    _name = 'res.partner.partner.type'
    _description = 'Res Partner partner Type'

    name = fields.Char(
        string="Nombre"
    )
    stakeholder = fields.Boolean(
        string="Stakeholder"
    )
    user = fields.Boolean(
        string="Usuario"
    ) 