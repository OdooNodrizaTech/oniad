# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, fields, models
from ..sendinblue.web_service import SendinblueWebService
_logger = logging.getLogger(__name__)


class SendinblueAttribute(models.Model):
    _name = 'sendinblue.attribute'
    _description = 'Sendinblue Attribute'

    name = fields.Char(
        string='Name'
    )
    category = fields.Char(
        string='Category'
    )
    sendinblue_type = fields.Char(
        string='Type'
    )
    sendinblue_enumeration_ids = fields.Many2many(
        comodel_name='sendinblue.enumeration',
        string='Values'
    )
    calculated_value = fields.Char(
        string='Calculated value'
    )

    @api.model
    def cron_get_attributes(self):
        sendinblue_web_service = SendinblueWebService(
            self.env.user.company_id,
            self.env
        )
        return_get_attributes = sendinblue_web_service.get_attributes()
        if not return_get_attributes['errors']:
            if len(return_get_attributes['response'].attributes) > 0:
                # fix enumeration
                for attribute in return_get_attributes['response'].attributes:
                    if attribute.enumeration is not None:
                        for enumeration_item in attribute.enumeration:
                            se_ids = self.env['sendinblue.enumeration'].search(
                                [
                                    ('label', '=', enumeration_item.label),
                                    ('value', '=', enumeration_item.value)
                                ]
                            )
                            if len(se_ids) == 0:
                                vals = {
                                    'label': enumeration_item.label,
                                    'value': enumeration_item.value,                                                                                                                 
                                }                        
                                self.env['sendinblue.enumeration'].sudo().create(
                                    vals
                                )
                # attributes
                for attribute in return_get_attributes['response'].attributes:
                    # attribute
                    sa_ids = self.env['sendinblue.attribute'].search(
                        [
                            ('name', '=', attribute.name)
                        ]
                    )
                    if sa_ids:
                        sa_obj = sa_ids[0]
                        # sendinblue_enumeration_ids
                        sendinblue_enumeration_ids = []
                        if attribute.enumeration is not None:
                            for enumeration_item in attribute.enumeration:   
                                se_ids_get = self.env['sendinblue.enumeration'].search(
                                    [
                                        ('label', '=', enumeration_item.label),
                                        ('value', '=', enumeration_item.value)
                                    ]
                                )
                                if se_ids_get:
                                    se_id_get = se_ids_get[0]
                                    sendinblue_enumeration_ids.append(se_id_get.id)
                        
                        sa_obj.update({
                            'name': attribute.name,
                            'category': attribute.category,
                            'sendinblue_type': attribute.type,
                            'calculated_value': attribute.calculated_value,
                            'sendinblue_enumeration_ids': sendinblue_enumeration_ids,
                        })                                                                                                                                                                                                                                        
                    else:
                        vals = {
                            'name': attribute.name,
                            'category': attribute.category,
                            'sendinblue_type': attribute.type,
                            'calculated_value': attribute.calculated_value,                                                                                                                 
                        }                        
                        self.env['sendinblue.attribute'].sudo().create(vals)
