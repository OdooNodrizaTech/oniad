# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    oniad_campaign_id = fields.Many2one(
        comodel_name='oniad.campaign',
        string='Oniad Campaign'
    )
    oniad_user_id_link = fields.Char(
        compute='_oniad_user_id_link',
        string='OniAd User',
        store=False
    )
    
    @api.multi        
    def _oniad_user_id_link(self):
        for record in self:
            if record.partner_id.id>0:
                if record.partner_id.oniad_user_id.id>0:
                    record.oniad_user_id_link = 'https://platform.oniad.com/backend/admin/supadmin/card/'+str(record.partner_id.oniad_user_id.id)