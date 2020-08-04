# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerStakeholderType(models.Model):
    _name = 'res.partner.stakeholder.type'
    _description = 'Res Partner Stakeholder Type'

    name = fields.Char(
        string="Name"
    )
    fan = fields.Boolean(
        string="Fan"
    )
    investor = fields.Boolean(
        string="Inverstor"
    )
    teacher = fields.Boolean(
        string="Teacher"
    )
    association = fields.Boolean(
        string="Association"
    )
    communicator = fields.Boolean(
        string="Communicator"
    )
