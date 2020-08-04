# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SendinblueContactAttribute(models.Model):
    _name = 'sendinblue.contact.attribute'
    _description = 'Sendinblue Contact Attribute'

    sendinblue_contact_id = fields.Many2one(
        comodel_name='sendinblue.contact',
        string='Sendinblue Contact'
    )
    sendinblue_attribute_id = fields.Many2one(
        comodel_name='sendinblue.attribute',
        string='Sendinblue Attribute'
    )
    sendinblue_enumeration_id = fields.Many2one(
        comodel_name='sendinblue.enumeration',
        string='Sendinblue Enumeration'
    )
    value = fields.Char(
        string='Value'
    )
