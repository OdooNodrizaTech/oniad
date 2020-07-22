# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerAgencyType(models.Model):
    _name = 'res.partner.agency.type'
    _description = 'Res Partner Agency Type'

    name = fields.Char(
        string="Name"
    )     