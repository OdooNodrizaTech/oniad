# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartnerCommunicationGeo(models.Model):
    _name = 'res.partner.communication.geo'
    _description = 'Res Partner Communication Geo'

    name = fields.Char(
        string="Nombre"
    )     