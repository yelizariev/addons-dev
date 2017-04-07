# -*- coding: utf-8 -*-
# Copyright 2017 IT-Projects LLC (<https://it-projects.info>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import models, fields, api


class User(models.Model):

    _name = 'apps_odoo_com.user'
    name = fields.Char(readonly=True)
    odoo_id = fields.Integer(readonly=True)


class Module(models.Model):

    _name = 'apps_odoo_com.module'
    name = fields.Char(readonly=True)
    odoo_id = fields.Integer(readonly=True)
    version = fields.Char(index=True, readonly=True)


class Purchase(models.Model):
    """Copy of records loempia.module.purchase from apps.odoo.com"""

    _name = 'apps_odoo_com.purchase'

    odoo_id = fields.Integer(readonly=True)

    #id = fields.Integer(readonly=True)
    purchase_order_ref = fields.Char(readonly=True)
    #display_name = fields.Char(readonly=True)
    user_id = fields.Many2one('apps_odoo_com.user', string="Buyer", readonly=True, index=True)
    product_id = fields.Char(readonly=True)
    referrer_module_id = fields.Many2one('apps_odoo_com.module', string="Referrer Module", readonly=True)
    last_update = fields.Datetime(readonly=True)
    order_id = fields.Char(readonly=True)
    price_unit = fields.Float(readonly=True)
    price = fields.Float(readonly=True)
    order_name = fields.Char(readonly=True)
    state = fields.Char(readonly=True)
    #module_maintainer_id = fields.Char(readonly=True)
    module_id = fields.Many2one('apps_odoo_com.module', string="Module", readonly=True)
    date_order = fields.Char(readonly=True)
    quantity = fields.Float(readonly=True)
