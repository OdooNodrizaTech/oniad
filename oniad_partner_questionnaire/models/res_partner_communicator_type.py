# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class ResPartnerCommunicatorType(models.Model):
    _name = 'res.partner.communicator.type'

    name = fields.Char(
        string="Nombre"
    )
    influencer = fields.Boolean(
        string="Influencer"
    )     