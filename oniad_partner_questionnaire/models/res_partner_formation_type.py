# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerFormationType(models.Model):
    _name = 'res.partner.formation.type'
    _description = 'Res Partner Formation Type'

    name = fields.Char(
        string="Name"
    )     