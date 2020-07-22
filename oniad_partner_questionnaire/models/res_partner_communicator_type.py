# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerCommunicatorType(models.Model):
    _name = 'res.partner.communicator.type'
    _description = 'Res Partner Communicator Type'

    name = fields.Char(
        string="Name"
    )
    influencer = fields.Boolean(
        string="Influencer"
    )     