# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerInversorType(models.Model):
    _name = 'res.partner.inversor.type'
    _description = 'Res Partner Inversor Type'

    name = fields.Char(
        string="Name"
    )
