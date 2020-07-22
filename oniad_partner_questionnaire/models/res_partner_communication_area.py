# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerCommunicationArea(models.Model):
    _name = 'res.partner.communication.area'
    _description = 'Res Partner Communication Area'

    name = fields.Char(
        string="Name"
    )     