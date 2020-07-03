# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerCustomerType(models.Model):
    _name = 'res.partner.customer.type'
    _description = 'Res Partner Customer Type'

    name = fields.Char(
        string="Nombre"
    )     
    advertiser = fields.Boolean(
        string="Anunciante"
    )
    agency = fields.Boolean(
        string="Agencia"
    )