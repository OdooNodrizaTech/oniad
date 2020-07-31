# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerSocialNetwork(models.Model):
    _name = 'res.partner.social.network'
    _description = 'Res Partner Social Network'

    name = fields.Char(
        string="Name"
    )
