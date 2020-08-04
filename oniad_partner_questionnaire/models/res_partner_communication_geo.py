# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerCommunicationGeo(models.Model):
    _name = 'res.partner.communication.geo'
    _description = 'Res Partner Communication Geo'

    name = fields.Char(
        string="Name"
    )
