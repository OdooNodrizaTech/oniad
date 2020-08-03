# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import Warning as UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
            
    sale_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Sale user id'
    )
    oniad_contact_use = fields.Selection(
        selection=[
            ('none', 'None'),
            ('communications', 'Communications')
        ],
        default='none',
        string='Oniad contact use'
    )
    
    @api.multi
    def write(self, vals):
        allow_write = True
        # check_dni
        if self.type == 'contact' and self.parent_id.id == 0:
            if 'vat' in vals:
                if not vals['vat']:
                    vals['vat'] = vals['vat'].strip().replace(' ', '').upper()
                
                    if self.country_id and self.country_id.code == 'ES':
                        if '-' in vals['vat']:
                            allow_write = False
                            raise UserError(_('Nif not allow character -'))
                                                    
        if allow_write:
            return super(ResPartner, self).write(vals)
