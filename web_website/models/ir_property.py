# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields


class IrProperty(models.Model):

    _inherit = 'ir.property'

    website_id = fields.Many2one('website', 'Website')
