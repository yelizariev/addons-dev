# -*- coding: utf-8 -*-
from openerp import models, fields, api


CUSTOM_CSS_ARCH = '''<?xml version="1.0"?>
<t t-name="theme_kit.custom_css">
%s
</t>
'''

class Config(models.Model):

    _name = 'theme_kit.config'
    _inherit = 'res.config.settings'

    theme_id = fields.Many2one('theme_kit.theme', string="Color Scheme")

    @api.multi
    def set_theme(self):
        custom_css = self.env.ref('theme_kit.custom_css')
        html = ''
        if self.theme_id:
            html = self.theme_id.html
        arch = CUSTOM_CSS_ARCH % html
        custom_css.write({'arch': arch})



