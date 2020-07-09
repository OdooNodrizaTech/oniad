# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerMarketTarget(models.Model):
    _name = 'res.partner.market.target'
    _description = 'Res Partner Market Target'

    name = fields.Char(
        string="Name"
    )     