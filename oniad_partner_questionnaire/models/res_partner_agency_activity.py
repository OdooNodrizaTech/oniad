# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerAgencyActivity(models.Model):
    _name = 'res.partner.agency.activity'

    name = fields.Char(
        string="Nombre"
    )     