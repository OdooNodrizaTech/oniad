# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerEducationalCenterType(models.Model):
    _name = 'res.partner.educational.center.type'
    _description = 'Res Partner Educational Center Type'

    name = fields.Char(
        string="Name"
    )     