# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerActivity(models.Model):
    _name = 'res.partner.activity'
    _description = 'Res Partner Activity'

    name = fields.Char(
        string="Name"
    )
    res_partner_sector_id = fields.Many2one(
        comodel_name='res.partner.sector',         
        string='Sector',
    )     