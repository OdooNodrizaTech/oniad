# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerPartnerType(models.Model):
    _name = 'res.partner.partner.type'
    _description = 'Res Partner partner Type'

    name = fields.Char(
        string="Name"
    )
    stakeholder = fields.Boolean(
        string="Stakeholder"
    )
    user = fields.Boolean(
        string="User"
    ) 