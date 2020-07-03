# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerSocialNetwork(models.Model):
    _name = 'res.partner.social.network'

    name = fields.Char(
        string="Nombre"
    )     