# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerFanLevel(models.Model):
    _name = 'res.partner.fan.level'
    _description = 'Res Partner Fan Level'

    name = fields.Char(
        string="Name"
    )     