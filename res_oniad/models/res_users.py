# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields
from openerp.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    commercial_phone = fields.Char( 
        string='Telefono'
    )
    oniad_code = fields.Integer( 
        string='Codigo Oniad'
    )