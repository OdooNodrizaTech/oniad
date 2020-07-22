# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerAsociationGeo(models.Model):
    _name = 'res.partner.asociation.geo'
    _description = 'Res Partner Asociation Geo'

    name = fields.Char(
        string="Name"
    )     