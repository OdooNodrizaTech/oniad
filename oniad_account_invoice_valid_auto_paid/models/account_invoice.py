# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, _

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    def action_invoice_open(self):
        # action
        return_action = super(AccountInvoice, self).action_invoice_open()
        # operations
        for item in self:
            if item.amount_total != 0:
                if item.type in ['out_invoice', 'out_refund']:
                    ids = []
                    for invoice_line_id in item.invoice_line_ids:
                        if invoice_line_id.oniad_transaction_id:
                            if invoice_line_id.oniad_transaction_id.id not in ids:
                                ids.append(
                                    int(invoice_line_id.oniad_transaction_id.id)
                                )
                    # check
                    if len(oniad_transaction_ids) > 0:
                        transaction_ids = self.env['oniad.transaction'].sudo().search(
                            [
                                ('id', 'in', ids),
                                ('account_payment_id', '!=', False)
                            ]
                        )
                        if transaction_ids:
                            for transaction_id in transaction_ids:
                                payment_id = transaction_id.account_payment_id
                                if payment_id.payment_type == 'inbound':
                                    for move_line_id in payment_id.move_line_ids:
                                        if move_line_id.credit > 0:
                                            _logger.info(
                                                _('Factura %s pre-asignar asiento '
                                                  'contable %s del pago %s')
                                                % (
                                                    item.id,
                                                    move_line_id.id,
                                                    payment_id.id
                                                )
                                            )
                                            item.assign_outstanding_credit(
                                                move_line_id.id
                                            )
                                            _logger.info(
                                                _('Factura %s asignado asiento '
                                                  'contable %s del pago %s')
                                                % (
                                                    item.id,
                                                    move_line_id.id,
                                                    payment_id.id
                                                )
                                            )
                                elif payment_id.payment_type == 'outbound':
                                    for move_line_id in payment_id.move_line_ids:
                                        if move_line_id.debit > 0:
                                            _logger.info(
                                                _('Factura %s pre-asignar asiento '
                                                  'contable %s del pago %s')
                                                % (
                                                    item.id,
                                                    move_line_id.id,
                                                    payment_id.id
                                                )
                                            )
                                            item.assign_outstanding_credit(
                                                move_line_id.id
                                            )
                                            _logger.info(
                                                _('Factura %s asignado asiento '
                                                  'contable %s del pago %s')
                                                % (
                                                    item.id,
                                                    move_line_id.id,
                                                    payment_id.id
                                                )
                                            )
        # return
        return return_action
