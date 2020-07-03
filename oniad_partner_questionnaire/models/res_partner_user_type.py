# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerUserType(models.Model):
    _name = 'res.partner.user.type'
    _description = 'res.partner.user.type'

    name = fields.Char(
        string="Nombre"
    )     