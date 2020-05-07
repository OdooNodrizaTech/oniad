# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerAgencyActivity(models.Model):
    _name = 'res.partner.agency.activity'
    _description = 'Res Partner Agency Activity'

    name = fields.Char(
        string="Nombre"
    )     