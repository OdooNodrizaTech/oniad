# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api,  models
from dateutil.relativedelta import relativedelta
from datetime import datetime

import uuid
import pytz

import logging
_logger = logging.getLogger(__name__)


class SurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'

    @api.multi
    def oniad_send_partner_mails(self, items, cr=None, uid=False, context=None):
        self.ensure_one()
        # create_survey_user_input_by_oniad_user_id

        def create_survey_user_input_by_oniad_user_id(
                survey_survey,
                partner,
                oniad_user_id
        ):
            response_ids = self.env['survey.user_input'].search([
                ('survey_id', '=', survey_survey.id),
                ('state', 'in', ['new', 'skip']),
                ('oniad_user_id', '=', oniad_user_id.id),
                '|',
                ('partner_id', '=', partner.id),
                ('email', '=', partner.email)]
            )
            if response_ids:
                return response_ids[0]

            token = uuid.uuid4().__str__()
            # create response with token
            vals = {
                'survey_id': survey_survey.id,
                'date_create': datetime.now(),
                'type': 'link',
                'state': 'new',
                'token': token,
                'oniad_user_id': oniad_user_id.id,
                'user_id': partner.user_id.id,
                'partner_id': partner.id,
                'email': partner.email
            }
            # deadline
            if survey_survey.deadline_days > 0:
                current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                deadline = current_date + relativedelta(
                    days=survey_survey.deadline_days
                )
                vals['deadline'] = deadline
            # survey_user_input_obj
            return self.env['survey.user_input'].sudo().create(vals)

        # create_survey_user_input_by_oniad_campaign_id
        def create_survey_user_input_by_oniad_campaign_id(
                survey_survey,
                partner,
                oniad_campaign_id
        ):
            response_ids = self.env['survey.user_input'].search([
                ('survey_id', '=', survey_survey.id),
                ('state', 'in', ['new', 'skip']),
                ('oniad_campaign_id', '=', oniad_campaign_id.id),
                '|',
                ('partner_id', '=', partner.id),
                ('email', '=', partner.email)]
            )
            if response_ids:
                return response_ids[0]

            token = uuid.uuid4().__str__()
            # create response with token
            vals = {
                'survey_id': survey_survey.id,
                'date_create': datetime.now(),
                'type': 'link',
                'state': 'new',
                'token': token,
                'oniad_campaign_id': oniad_campaign_id.id,
                'oniad_user_id': oniad_campaign_id.oniad_user_id.id,
                'user_id': partner.user_id.id,
                'partner_id': partner.id,
                'email': partner.email
            }
            # deadline
            if survey_survey.deadline_days > 0:
                current_date = datetime.now(pytz.timezone('Europe/Madrid'))
                deadline = current_date + relativedelta(
                    days=survey_survey.deadline_days
                )
                vals['deadline'] = deadline
            # survey_user_input_obj
            return self.env['survey.user_input'].sudo().create(vals)

        def create_response_and_send_mail(
                smcm,
                sui
        ):
            # url
            url = '%s/%s' % (
                sui.survey_id.public_url,
                sui.token
            )
            vals = {
                'auto_delete': True,
                'model': 'survey.user_input',
                'res_id': sui.id,
                'subject': self.subject,
                'body': smcm.body.replace("__URL__", url),
                'body_html': smcm.body.replace("__URL__", url),
                'record_name': sui.survey_id.title,
                'no_auto_thread': False,
                'reply_to': smcm.reply_to,
                'message_type': 'email',
                'email_from': smcm.email_from,
                'email_to': sui.partner_id.email,
                'partner_ids':
                    sui.partner_id.id and [(4, sui.partner_id.id)] or None
            }
            mail_mail_obj = self.env['mail.mail'].sudo().create(vals)
            mail_mail_obj.send()
            self.action_send_survey_mail_message_slack(sui)

        survey_ids = self.env['survey.survey'].search(
            [
                ('id', '=', str(self.survey_id.id))
            ]
        )
        survey_id = survey_ids[0]
        for partner_id in self.partner_ids:
            partner_id_item = items[partner_id.id]
            # create_survey_user_input_by_oniad_user_id
            if 'oniad_user_id' in partner_id_item:
                sui = \
                    create_survey_user_input_by_oniad_user_id(
                        survey_id,
                        partner_id,
                        partner_id_item['oniad_user_id']
                    )
            # create_survey_user_input_by_oniad_campaign_id
            if 'oniad_campaign_id' in partner_id_item:
                sui = \
                    create_survey_user_input_by_oniad_campaign_id(
                        survey_id,
                        partner_id,
                        partner_id_item['oniad_campaign_id']
                    )
            # create_response_and_send_mail
            create_response_and_send_mail(self, sui)
            # save_log
            vals = {
                'model': 'survey.user_input',
                'res_id': sui.id,
                'category': 'survey_user_input',
                'action': 'send_mail'
            }
            self.env['automation.log'].sudo().create(vals)
