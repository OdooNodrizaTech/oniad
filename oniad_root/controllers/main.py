# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import werkzeug

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.website_mail.controllers.main import _message_post_helper

import logging
_logger = logging.getLogger(__name__)

class OniadAddressController(http.Controller):
    
    @http.route("/oniad_address/<int:oniad_address_id>", type='http', auth="user", website=True)
    def oniad_address_view(self, *args, **kwargs):
        if 'oniad_address_id' not in kwargs:
            return request.render('website.404')
        else:
            oniad_address_ids = request.env['oniad.address'].sudo().search([('id', '=', kwargs['oniad_address_id'])])
            if len(oniad_address_ids)==0:
                return request.render('website.404')
            else:
                oniad_address_id = oniad_address_ids[0]
                if oniad_address_id.partner_id.id==0:
                    return request.render('website.404')
                else:
                    return request.redirect('/web?&#id=%s&view_type=form&model=res.partner' %(oniad_address_id.partner_id.id))
                    
class OniadUserController(http.Controller):
    
    @http.route("/oniad_user/<int:oniad_user_id>", type='http', auth="user", website=True)
    def oniad_user_view(self, *args, **kwargs):
        if 'oniad_user_id' not in kwargs:
            return request.render('website.404')
        else:
            oniad_user_ids = request.env['oniad.user'].sudo().search([('id', '=', kwargs['oniad_user_id'])])
            if len(oniad_user_ids)==0:
                return request.render('website.404')
            else:
                oniad_user_id = oniad_user_ids[0]
                if oniad_user_id.partner_id.id==0:
                    return request.render('website.404')
                else:
                    return request.redirect('/web?&#id=%s&view_type=form&model=res.partner' %(oniad_user_id.partner_id.id))                                        