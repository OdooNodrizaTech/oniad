# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sendinblue_contact_id = fields.Many2one(
        comodel_name='sendinblue.contact',
        string='Sendinblue Contacto'
    )
    sendinblue_list_id = fields.Many2one(
        comodel_name='sendinblue.list',
        string='Sendinblue Lista'
    )
    
    @api.one    
    def action_leads_create_sendinblue_list_id(self):
        return True                    