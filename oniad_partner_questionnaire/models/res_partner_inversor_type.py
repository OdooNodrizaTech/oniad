# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerInversorType(models.Model):
    _name = 'res.partner.inversor.type'

    name = fields.Char(
        string="Nombre"
    )     