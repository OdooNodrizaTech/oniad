# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from ..sendinblue.web_service import SendinblueWebService

class SendinblueContact(models.Model):
    _name = 'sendinblue.contact'
    _description = 'Sendinblue Contact'    
    
    sendinblue_id = fields.Char(        
        string='Sendinblue Id'
    )
    email = fields.Char(        
        string='Email'
    )
    email_blacklisted = fields.Boolean(        
        string='Email blacklisted'
    )    
    sms_blacklisted = fields.Boolean(        
        string='Sms blacklisted'
    )
    modified_at = fields.Date(        
        string='Modificadl el'
    )
    sendinblue_list_ids = fields.Many2many(
        comodel_name='sendinblue.list',
        string='Listas'
    )    
    
    @api.model    
    def cron_auto_generate_leads_sendinblue(self):
        oniad_sendinblue_auto_generate_leads_sendinblue_list_id = str(self.env['ir.config_parameter'].sudo().get_param('oniad_sendinblue_auto_generate_leads_sendinblue_list_id'))
        user_id_default = str(self.env['ir.config_parameter'].sudo().get_param('oniad_sendinblue_auto_generate_leads_user_id_default'))
        leads_tag_ids_default = str(self.env['ir.config_parameter'].sudo().get_param('oniad_sendinblue_auto_generate_leads_tag_ids_default'))                                
        
        if oniad_sendinblue_auto_generate_leads_sendinblue_list_id>0:
            #res_users
            res_user_ids = self.env['res.users'].search([('id', '=', user_id_default)])
            res_user_id = res_user_ids[0]
            #crm_team
            crm_team_ids = self.env['crm.team'].search([('id', '=', res_user_id.sale_team_id.id)])
            crm_team_id = crm_team_ids[0]
            #crm_stage
            crm_stage_ids = self.env['crm.stage'].search([('id', '=', 1)])
            crm_stage_id = crm_stage_ids[0]
            #tag_ids
            tag_ids = []
            tag_ids_split = leads_tag_ids_default.split(',')
            for tag_id_split in tag_ids_split:
                tag_ids.append(int(tag_id_split))
        
            sendinblue_contact_ids_real = []
            sendinblue_contact_ids_already_created = []
            
            sendinblue_contact_ids = self.env['sendinblue.contact'].search([
                ('sendinblue_list_ids', 'in', [oniad_sendinblue_auto_generate_leads_sendinblue_list_id])
            ])
            if len(sendinblue_contact_ids)>0:
                for sendinblue_contact_id in sendinblue_contact_ids:
                    sendinblue_contact_ids_real.append(sendinblue_contact_id.id)
                                                
                crm_lead_ids = self.env['crm.lead'].search([
                    ('sendinblue_contact_id', 'in', sendinblue_contact_ids_real)
                ])
                if len(crm_lead_ids)>0:
                    for crm_lead_id in crm_lead_ids:
                        sendinblue_contact_ids_already_created.append(crm_lead_id.sendinblue_contact_id.id)
                
                for sendinblue_contact_id in sendinblue_contact_ids:
                    if sendinblue_contact_id.id not in sendinblue_contact_ids_already_created:
                        #default_fields
                        crm_type = 'lead'
                        commercial_activity_type = 'hunter'
                        lead_oniad_type = 'catchment'
                        
                        crm_partner_id = False
                        partner_name = sendinblue_contact_id.email                        
                        stage_id = 0                        
                        #res_partner
                        res_partner_ids = self.env['res.partner'].search([
                            ('active', '=', True),
                            ('email', '=', sendinblue_contact_id.email)
                        ])
                        if len(res_partner_ids)!=0:
                            for res_partner_id in res_partner_ids:
                                if res_partner_id.oniad_user_id>0:
                                    crm_type = 'opportunity'
                                    commercial_activity_type = 'account'
                                    lead_oniad_type = 'other'
                                    #extra
                                    crm_partner_id = res_partner_id.id
                                    partner_name = res_partner_id.name
                                    stage_id = crm_stage_id.id                                                   
                        
                        crm_lead_vals = {
                            'name': sendinblue_contact_id.email,
                            'partner_name': partner_name,
                            'contact_name': partner_name,
                            'email_from': sendinblue_contact_id.email,
                            'sendinblue_contact_id': sendinblue_contact_id.id,
                            'sendinblue_list_id': oniad_sendinblue_auto_generate_leads_sendinblue_list_id,
                            'commercial_activity_type': commercial_activity_type,
                            'lead_oniad_type': lead_oniad_type,
                            'type': crm_type,
                            'partner_id': crm_partner_id,
                            'team_id': crm_team_id.id,
                            'stage_id': stage_id,
                            'user_id': res_user_id.id,
                            'marketing_campaing': True,
                            'active': True,
                            'tag_ids': [(6, 0, tag_ids)],                                                                                                                 
                        }                        
                        crm_lead_obj = self.env['crm.lead'].sudo(res_user_id.id).create(crm_lead_vals)
                        crm_lead_obj.action_leads_create_sendinblue_list_id()#log_slack                                                                                                
    
    @api.model    
    def cron_get_contacts(self):
        sendinblue_web_service = SendinblueWebService(self.env.user.company_id, self.env)
        return_get_contacts = sendinblue_web_service.get_contacts()                
        if return_get_contacts['errors']==False:
            if return_get_contacts['response']['count']>0:
                for contact in return_get_contacts['response']['contacts']:
                    #sendinblue_list_ids
                    sendinblue_list_ids = []
                    if len(contact['listIds'])>0:
                        sendinblue_list_ids_get = self.env['sendinblue.list'].search([('sendinblue_id', 'in', contact['listIds'])])
                        if len(sendinblue_list_ids_get)>0:
                            for sendinblue_list_id_get in sendinblue_list_ids_get:
                                sendinblue_list_ids.append(sendinblue_list_id_get.id)                                                                                    
                    #contact_item                                                        
                    sendinblue_contact_ids = self.env['sendinblue.contact'].search([('sendinblue_id', '=', contact['id'])])
                    if len(sendinblue_contact_ids)>0:
                        sendinblue_contact_obj = sendinblue_contact_ids[0]
                        #attributes
                        if "attributes" in contact:
                            if len(contact['attributes'])>0:
                                for attribute_key, attribute_val in contact['attributes'].items():
                                    sendinblue_attribute_ids = self.env['sendinblue.attribute'].search([('name', '=', attribute_key)])
                                    if len(sendinblue_attribute_ids)>0:
                                        sendinblue_attribute_id = sendinblue_attribute_ids[0]
                                        sendinblue_enumeration_id = False
                                        
                                        if len(sendinblue_attribute_id.sendinblue_enumeration_ids)>0:
                                            for sendinblue_enumeration_id in sendinblue_attribute_id.sendinblue_enumeration_ids:
                                                if sendinblue_enumeration_id.value==attribute_val:
                                                    sendinblue_enumeration_id = sendinblue_enumeration_id.id                                               
                                
                                        sendinblue_contact_attribute_ids_get = self.env['sendinblue.contact.attribute'].search([('sendinblue_contact_id', '=', sendinblue_contact_obj.id),('sendinblue_attribute_id', '=', sendinblue_attribute_id.id)])                                        
                                        if len(sendinblue_contact_attribute_ids_get)==0:
                                            sendinblue_contact_attribute_vals = {
                                                'sendinblue_contact_id': sendinblue_contact_obj.id,
                                                'sendinblue_attribute_id': sendinblue_attribute_id.id,
                                                'sendinblue_enumeration_id': sendinblue_enumeration_id,
                                                'value': attribute_val,                                                                                                                 
                                            }                        
                                            sendinblue_contact_attribute_obj = self.env['sendinblue.contact.attribute'].sudo().create(sendinblue_contact_attribute_vals)                                                                
                        #update
                        sendinblue_contact_obj.update({
                            'sendinblue_id': contact['id'],
                            'email': contact['email'],
                            'email_blacklisted': contact['emailBlacklisted'],
                            'sms_blacklisted': contact['smsBlacklisted'],
                            'modified_at': contact['modifiedAt'],
                            'sendinblue_list_ids': sendinblue_list_ids,
                        })                        
                    else:
                        sendinblue_contact_vals = {
                            'sendinblue_id': contact['id'],
                            'email': contact['email'],
                            'email_blacklisted': contact['emailBlacklisted'],
                            'sms_blacklisted': contact['smsBlacklisted'],
                            'modified_at': contact['modifiedAt'],                                                                                                                 
                        }                        
                        sendinblue_contact_obj = self.env['sendinblue.contact'].sudo().create(sendinblue_contact_vals)                                                