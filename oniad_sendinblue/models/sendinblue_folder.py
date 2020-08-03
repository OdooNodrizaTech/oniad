# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from ..sendinblue.web_service import SendinblueWebService

class SendinblueFolder(models.Model):
    _name = 'sendinblue.folder'
    _description = 'Sendinblue Folder'    
    
    sendinblue_id = fields.Char(
        string='Sendinblue Id'
    )
    name = fields.Char(
        string='Name'
    )
    total_blacklisted = fields.Integer(
        string='Total blacklisted'
    )
    total_subscribers = fields.Integer(
        string='Total suscriptores'
    )
    unique_subscribers = fields.Integer(
        string='Unique subscribers'
    )
    
    @api.model    
    def cron_get_folders(self):
        sendinblue_web_service = SendinblueWebService(self.env.user.company_id, self.env)
        res = sendinblue_web_service.get_folders()
        if not res['errors']:
            if res['response'].count > 0:
                for folder in res['response'].folders:
                    sendinblue_folder_ids = self.env['sendinblue.folder'].search(
                        [
                            ('sendinblue_id', '=', folder['id'])
                        ]
                    )
                    if sendinblue_folder_ids:
                        sendinblue_folder_obj = sendinblue_folder_ids[0]
                        
                        sendinblue_folder_obj.update({
                            'sendinblue_id': folder['id'],
                            'name': folder['name'],
                            'total_blacklisted': folder['totalBlacklisted'],
                            'total_subscribers': folder['totalSubscribers'],
                            'unique_subscribers': folder['uniqueSubscribers'],
                        })                        
                    else:
                        vals = {
                            'sendinblue_id': folder['id'],
                            'name': folder['name'],
                            'total_blacklisted': folder['totalBlacklisted'],
                            'total_subscribers': folder['totalSubscribers'],
                            'unique_subscribers': folder['uniqueSubscribers']                                                                                                                 
                        }                        
                        self.env['sendinblue.folder'].sudo().create(vals)