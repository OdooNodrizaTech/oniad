# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerAgencyType(models.Model):
    _name = 'res.partner.agency.type'

    name = fields.Char(
        string="Nombre"
    )     