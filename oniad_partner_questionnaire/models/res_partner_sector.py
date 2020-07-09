# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerSector(models.Model):
    _name = 'res.partner.sector'
    _description = 'Res Partner Sector'

    name = fields.Char(
        string="Name"
    )     