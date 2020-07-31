# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import werkzeug

from odoo import fields, http, _
from odoo.http import request


class OniadAddressController(http.Controller):
    
    @http.route("/oniad_address/<int:oniad_address_id>",
                type='http',
                auth="user",
                website=True
                )
    def oniad_address_view(self, *args, **kwargs):
        if 'oniad_address_id' not in kwargs:
            return request.render('website.404')
        else:
            address_ids = request.env['oniad.address'].sudo().search(
                [
                    ('id', '=', kwargs['oniad_address_id'])
                ]
            )
            if len(address_ids) == 0:
                return request.render('website.404')
            else:
                if address_ids[0].partner_id.id == 0:
                    return request.render('website.404')
                else:
                    return request.redirect(
                        '/web?&#id=%s&view_type=form&model=res.partner'
                        % address_ids[0].partner_id.id
                    )
                    
class OniadUserController(http.Controller):
    
    @http.route("/oniad_user/<int:oniad_user_id>",
                type='http',
                auth="user",
                website=True
                )
    def oniad_user_view(self, *args, **kwargs):
        if 'oniad_user_id' not in kwargs:
            return request.render('website.404')
        else:
            user_ids = request.env['oniad.user'].sudo().search(
                [
                    ('id', '=', kwargs['oniad_user_id'])
                ]
            )
            if len(user_ids) == 0:
                return request.render('website.404')
            else:
                if user_ids[0].partner_id.id == 0:
                    return request.render('website.404')
                else:
                    return request.redirect(
                        '/web?&#id=%s&view_type=form&model=res.partner'
                        % user_ids[0].partner_id.id
                    )
