# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    oniad_address_id = fields.Many2one(
        comodel_name='oniad.address',
        compute='_compute_oniad_address_id',
        string='Oniad Address',
        store=True
    )
    oniad_transaction_count = fields.Integer(
        compute='_compute_oniad_transaction_count',
        string="Oniad Transactions",
    )

    @api.multi
    def _compute_oniad_transaction_count(self):
        for item in self:
            item.oniad_transaction_count = len(self.env['oniad.transaction'].search(
                [
                    ('account_invoice_id', '=', item.id)
                ]
            ))

    @api.multi
    @api.depends('partner_id.oniad_address_id')
    def _compute_oniad_address_id(self):
        for item in self:
            if item:
                if item.partner_id.oniad_address_id:
                    item.oniad_address_id = item.partner_id.oniad_address_id.id

    @api.multi
    def compute_taxes(self):
        return_object = super(AccountInvoice, self).compute_taxes()
        # update
        for obj in self:
            transaction_ids = []
            for line_id in obj.invoice_line_ids:
                if line_id.oniad_transaction_id:
                    transaction_ids.append(line_id.oniad_transaction_id.id)
            # Fix tax_line_ids
            if len(transaction_ids) > 0:
                # calculate
                tax_amount = 0
                tax_base = 0
                transaction_ids = self.env['oniad.transaction'].sudo().search(
                    [
                        ('id', 'in', transaction_ids)
                    ]
                )
                if transaction_ids:
                    for transaction_id in transaction_ids:
                        tax_amount += transaction_id.tax
                        tax_base += transaction_id.amount
                # update
                if obj.tax_line_ids:
                    obj.tax_line_ids[0].amount = tax_amount
                    obj.tax_line_ids[0].base = tax_base
        # return
        return return_object
