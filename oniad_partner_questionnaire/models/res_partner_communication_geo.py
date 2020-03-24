# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerCommunicationGeo(models.Model):
    _name = 'res.partner.communication.geo'

    name = fields.Char(
        string="Nombre"
    )     