# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerCommunicationArea(models.Model):
    _name = 'res.partner.communication.area'

    name = fields.Char(
        string="Nombre"
    )     