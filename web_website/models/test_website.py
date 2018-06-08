# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields


class WebsiteDependent(models.Model):
    _name = 'test.website'

    foo = fields.Char(company_dependent=True, website_dependent=True)
