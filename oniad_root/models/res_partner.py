# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, fields
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    oniad_user_id = fields.Many2one(
        comodel_name='oniad.user',
        string='Oniad User'
    )
    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        string='Oniad Address'
    )
    oniad_user_id_link = fields.Char(
        compute='_compute_oniad_user_id_link',
        string='OniAd User',
        store=False
    )

    @api.multi
    @api.depends('oniad_user_id')
    def _compute_oniad_user_id_link(self):
        for item in self:
            if item.id:
                if item.oniad_user_id:
                    item.oniad_user_id_link = '%s/backend/admin/supadmin/card/%s' \
                                              % (
                                                  'https://platform.oniad.com',
                                                  item.oniad_user_id.id
                                              )

    @api.model
    def check_vat_custom(self, vat=None):
        if self.env.context.get('company_id'):
            company = self.env['res.company'].browse(self.env.context['company_id'])
        else:
            company = self.env.user.company_id
        if company.vat_check_vies:
            # force full VIES online check
            check_func = self.vies_vat_check
        else:
            # quick and partial off-line checksum validation
            check_func = self.simple_vat_check

        if vat is None:
            return False

        vat_country, vat_number = self._split_vat(vat)
        if check_func(vat_country, vat_number):
            return True
        else:
            _logger.info(_("Importing VAT Number [%s] is not valid !") % vat_number)
            return False

    @api.multi
    def write(self, vals):
        send_sns_oniad_address_id_custom = False
        # customer_payment_mode_id
        if 'customer_payment_mode_id' in vals:
            customer_payment_mode_id_old = self.customer_payment_mode_id.id
        # property_payment_term_id
        if 'property_payment_term_id' in vals:
            property_payment_term_id_old = self.property_payment_term_id.id
        # super
        return_object = super(ResPartner, self).write(vals)
        # customer_payment_mode_id
        if 'customer_payment_mode_id' in vals:
            if self.customer_payment_mode_id.id != customer_payment_mode_id_old:
                send_sns_oniad_address_id_custom = True
        # property_payment_term_id
        if 'property_payment_term_id' in vals:
            if self.property_payment_term_id.id != property_payment_term_id_old:
                send_sns_oniad_address_id_custom = True
        # send
        if send_sns_oniad_address_id_custom:
            if self.oniad_address_id:
                self.oniad_address_id.action_send_sns()
        # return
        return return_object
