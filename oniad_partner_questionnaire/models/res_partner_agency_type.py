# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerAgencyType(models.Model):
    _name = 'res.partner.agency.type'
    _description = 'Res Partner Agency Type'

    name = fields.Char(
        string="Nombre"
    )     