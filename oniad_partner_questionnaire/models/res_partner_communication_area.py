# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerCommunicationArea(models.Model):
    _name = 'res.partner.communication.area'

    name = fields.Char(
        string="Nombre"
    )     