# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartnerStakeholderType(models.Model):
    _name = 'res.partner.stakeholder.type'

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