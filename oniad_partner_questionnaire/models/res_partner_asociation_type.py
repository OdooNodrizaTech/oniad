# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerAsociationType(models.Model):
    _name = 'res.partner.asociation.type'
    _description = 'Res Partner Asociation Type'

    name = fields.Char(
        string="Name"
    )
