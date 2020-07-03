# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerAgencyType(models.Model):
    _name = 'res.partner.agency.type'

    name = fields.Char(
        string="Nombre"
    )     