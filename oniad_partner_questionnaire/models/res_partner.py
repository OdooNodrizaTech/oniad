# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class ResPartnerCustom(models.Model):
    _inherit = 'res.partner'

    oa_qt_partner_type = fields.Many2many(
        comodel_name='res.partner.partner.type',
        string='Partner type',
    )

    @api.onchange('oa_qt_partner_type')
    def change_oa_qt_partner_type(self):
        self._get_oa_qt_show_stakeholder_tab()
        self._get_oa_qt_show_user_tab()

    # alculate field show_stakeholdert_tab
    oa_qt_show_stakeholder_tab = fields.Boolean(
        compute='_compute_oa_qt_show_stakeholder_tab',
        store=False
    )

    @api.multi
    def _compute_oa_qt_show_stakeholder_tab(self):
        for item in self:
            item.oa_qt_show_stakeholder_tab = False
            for oa_qt_partner_type in item.oa_qt_partner_type:
                if oa_qt_partner_type.stakeholder:
                    item.oa_qt_show_stakeholder_tab = True

    # calculate field user tab
    oa_qt_show_user_tab = fields.Boolean(
        compute='_compute_oa_qt_show_user_tab',
        store=False
    )

    @api.multi
    def _compute_oa_qt_show_user_tab(self):
        for item in self:
            item.oa_qt_show_user_tab = False
            for oa_qt_partner_type in item.oa_qt_partner_type:
                if oa_qt_partner_type.user:
                    item.oa_qt_show_user_tab = True

    oa_qt_stakeholder_type = fields.Many2many(
        comodel_name='res.partner.stakeholder.type',
        string='Stakeholder type',
    )

    @api.multi
    @api.onchange('oa_qt_stakeholder_type')
    def change_oa_qt_stakeholder_type(self):
        for item in self:
            item._get_oa_qt_is_fan()
            item._get_oa_qt_is_investor()
            item._get_oa_qt_is_teacher()
            item._get_oa_qt_is_association()
            item._get_oa_qt_is_communicator()
            item._get_oa_qt_is_communicator_influencer()

    # calculate field oa_qt_is_fan
    oa_qt_is_fan = fields.Boolean(
        compute='_compute_oa_qt_is_fan',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_fan(self):
        for item in self:
            item.oa_qt_is_fan = False
            for oa_qt_stakeholder_type in item.oa_qt_stakeholder_type:
                if oa_qt_stakeholder_type.fan:
                    item.oa_qt_is_fan = True

    # calculate field oa_qt_is_investor
    oa_qt_is_investor = fields.Boolean(
        compute='_compute_oa_qt_is_investor',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_investor(self):
        for item in self:
            item.oa_qt_is_investor = False
            for oa_qt_stakeholder_type in item.oa_qt_stakeholder_type:
                if oa_qt_stakeholder_type.investor:
                    item.oa_qt_is_investor = True

    # calculate field oa_qt_is_teacher
    oa_qt_is_teacher = fields.Boolean(
        compute='_compute_oa_qt_is_teacher',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_teacher(self):
        for item in self:
            item.oa_qt_is_teacher = False
            for oa_qt_stakeholder_type in item.oa_qt_stakeholder_type:
                if oa_qt_stakeholder_type.teacher:
                    item.oa_qt_is_teacher = True

    # calculate field oa_qt_is_association
    oa_qt_is_association = fields.Boolean(
        compute='_compute_oa_qt_is_association',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_association(self):
        for item in self:
            item.oa_qt_is_association = False
            for oa_qt_stakeholder_type in item.oa_qt_stakeholder_type:
                if oa_qt_stakeholder_type.association:
                    item.oa_qt_is_association = True

    # calculate field oa_qt_is_communicator
    oa_qt_is_communicator = fields.Boolean(
        compute='_compute_oa_qt_is_communicator',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_communicator(self):
        for item in self:
            item.oa_qt_is_communicator = False
            for oa_qt_stakeholder_type in item.oa_qt_stakeholder_type:
                if oa_qt_stakeholder_type.communicator:
                    item.oa_qt_is_communicator = True

    oa_qt_fan_level = fields.Many2many(
        comodel_name='res.partner.fan.level',
        string='Fan level',
    )
    oa_qt_inversor_type = fields.Many2many(
        comodel_name='res.partner.inversor.type',
        string='Inversor type',
    )
    oa_qt_educational_center_type = fields.Many2many(
        comodel_name='res.partner.educational.center.type',
        string='Educational center type',
    )
    oa_qt_formation_type = fields.Many2many(
        comodel_name='res.partner.formation.type',
        string='Formation type',
    )
    oa_qt_asociation_type = fields.Many2many(
        comodel_name='res.partner.asociation.type',
        string='Association type',
    )
    oa_qt_asociation_geo = fields.Many2many(
        comodel_name='res.partner.asociation.geo',
        string='Asociation geo',
    )
    oa_qt_communicator_type = fields.Many2many(
        comodel_name='res.partner.communicator.type',
        string='Communicator type',
    )

    @api.multi
    @api.onchange('oa_qt_communicator_type')
    def change_oa_qt_communicator_type(self):
        for item in self:
            item._get_oa_qt_is_communicator_influencer()

    # calculate field oa_qt_is_communicator_influencer
    oa_qt_is_communicator_influencer = fields.Boolean(
        compute='_compute_oa_qt_is_communicator_influencer',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_communicator_influencer(self):
        for item in self:
            item.oa_qt_is_communicator_influencer = False
            for oa_qt_communicator_type in item.oa_qt_communicator_type:
                if oa_qt_communicator_type.influencer:
                    item.oa_qt_is_communicator_influencer = True

    oa_qt_social_network = fields.Many2many(
        comodel_name='res.partner.social.network',
        string='Social network',
    )
    oa_qt_communication_area = fields.Many2many(
        comodel_name='res.partner.communication.area',
        string='Communication area',
    )
    oa_qt_communication_geo = fields.Many2many(
        comodel_name='res.partner.communication.geo',
        string='Communication geo',
    )
    oa_qt_user_type = fields.Many2one(
        comodel_name='res.partner.user.type',
        string='User type',
    )
    oa_qt_customer_type = fields.Many2one(
        comodel_name='res.partner.customer.type',
        string='Customer type',
    )

    @api.multi
    @api.onchange('oa_qt_customer_type')
    def change_oa_qt_customer_type(self):
        for item in self:
            item._get_oa_qt_is_advertiser()
            item._get_oa_qt_is_agency()

    # calculate field oa_qt_is_agency
    oa_qt_is_agency = fields.Boolean(
        compute='_compute_oa_qt_is_agency',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_agency(self):
        for item in self:
            item.oa_qt_is_agency = False
            for oa_qt_customer_type in item.oa_qt_customer_type:
                if oa_qt_customer_type.agency:
                    item.oa_qt_is_agency = True

    oa_qt_agency_type = fields.Many2many(
        comodel_name='res.partner.agency.type',
        string='Agency type',
    )
    # calculate field oa_qt_is_advertiser
    oa_qt_is_advertiser = fields.Boolean(
        compute='_compute_oa_qt_is_advertiser',
        store=False
    )

    @api.multi
    def _compute_oa_qt_is_advertiser(self):
        for item in self:
            item.oa_qt_is_advertiser = False
            for oa_qt_customer_type in item.oa_qt_customer_type:
                if oa_qt_customer_type.advertiser:
                    item.oa_qt_is_advertiser = True

    oa_qt_affiliate = fields.Boolean(
        string="Affiliate"
    )
    oa_qt_market_target = fields.Many2many(
        comodel_name='res.partner.market.target',
        string='Market target',
    )
    oa_qt_sector = fields.Many2one(
        comodel_name='res.partner.sector',
        string='Sector',
    )
    oa_qt_activity = fields.Many2many(
        comodel_name='res.partner.activity',
        string='Activity',
    )
    oa_qt_agency_activity = fields.Many2many(
        comodel_name='res.partner.agency.activity',
        string='Agency activity',
    )
