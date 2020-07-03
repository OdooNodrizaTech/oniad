# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerActivity(models.Model):
    _name = 'res.partner.activity'

    name = fields.Char(
        string="Nombre"
    )
    res_partner_sector_id = fields.Many2one(
        comodel_name='res.partner.sector',         
        string='Sector',
    )     