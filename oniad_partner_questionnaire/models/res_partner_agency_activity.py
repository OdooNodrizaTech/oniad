# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerAgencyActivity(models.Model):
    _name = 'res.partner.agency.activity'

    name = fields.Char(
        string="Nombre"
    )     