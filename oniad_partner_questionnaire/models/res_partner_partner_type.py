# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerPartnerType(models.Model):
    _name = 'res.partner.partner.type'

    name = fields.Char(
        string="Nombre"
    )
    stakeholder = fields.Boolean(
        string="Stakeholder"
    )
    user = fields.Boolean(
        string="Usuario"
    ) 