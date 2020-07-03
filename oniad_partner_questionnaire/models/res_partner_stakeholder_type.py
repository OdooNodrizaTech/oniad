# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class ResPartnerStakeholderType(models.Model):
    _name = 'res.partner.stakeholder.type'
    _description = 'Res Partner Stakeholder Type'

    name = fields.Char(
        string="Nombre"
    )
    fan = fields.Boolean(
        string="Fan"
    )
    investor = fields.Boolean(
        string="Inversor"
    )    
    teacher = fields.Boolean(
        string="Profesor"
    )
    association = fields.Boolean(
        string="Asociacion"
    )
    communicator = fields.Boolean(
        string="Comunicador"
    )     