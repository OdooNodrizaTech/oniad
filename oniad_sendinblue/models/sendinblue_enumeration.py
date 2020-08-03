# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SendinblueEnumeration(models.Model):
    _name = 'sendinblue.enumeration'
    _description = 'Sendinblue Enumeration'    
            
    label = fields.Char(
        string='Label'
    )
    value = fields.Integer(
        string='Value'
    )