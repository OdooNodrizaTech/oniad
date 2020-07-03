# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

from ..sendinblue.web_service import SendinblueWebService

class SendinblueFolder(models.Model):
    _name = 'sendinblue.folder'    
    
    sendinblue_id = fields.Char(        
        string='Sendinblue Id'
    )
    name = fields.Char(        
        string='Nombre'
    )
    total_blacklisted = fields.Integer(        
        string='Total blacklisted'
    )
    total_subscribers = fields.Integer(        
        string='Total suscriptores'
    )
    unique_subscribers = fields.Integer(        
        string='Suscriptores unicos'
    )
    
    @api.multi    
    def cron_get_folders(self, cr=None, uid=False, context=None):
        sendinblue_web_service = SendinblueWebService(self.env.user.company_id, self.env)
        return_get_folders = sendinblue_web_service.get_folders()
        if return_get_folders['errors']==False:
            if return_get_folders['response'].count>0:
                for folder in return_get_folders['response'].folders:
                    sendinblue_folder_ids = self.env['sendinblue.folder'].search([('sendinblue_id', '=', folder['id'])])
                    if len(sendinblue_folder_ids)>0:
                        sendinblue_folder_obj = sendinblue_folder_ids[0]
                        
                        sendinblue_folder_obj.update({
                            'sendinblue_id': folder['id'],
                            'name': folder['name'],
                            'total_blacklisted': folder['totalBlacklisted'],
                            'total_subscribers': folder['totalSubscribers'],
                            'unique_subscribers': folder['uniqueSubscribers'],
                        })                        
                    else:
                        sendinblue_folder_vals = {
                            'sendinblue_id': folder['id'],
                            'name': folder['name'],
                            'total_blacklisted': folder['totalBlacklisted'],
                            'total_subscribers': folder['totalSubscribers'],
                            'unique_subscribers': folder['uniqueSubscribers']                                                                                                                 
                        }                        
                        sendinblue_folder_obj = self.env['sendinblue.folder'].sudo().create(sendinblue_folder_vals)