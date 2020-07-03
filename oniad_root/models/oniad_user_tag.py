# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class OniadUserTag(models.Model):
    _name = 'oniad.user.tag'
    _description = 'Oniad User Tag'
    
    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User Id'
    )
    tag = fields.Char(
        string='Nombre'
    )                         