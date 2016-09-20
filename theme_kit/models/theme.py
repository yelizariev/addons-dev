# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Theme(models.Model):
    _name = "theme_kit.theme"

    name = fields.Char('Name')
    main_menu_navbar_bg = fields.Char('Background color', help="Color for Main Menu Bar")
    html = fields.Text('Html', help='technical computed field', compute='_compute_html')

    @api.multi
    def _compute_html(self):
        for r in self:
            # double {{ will be formated as single {
            html = '''
<style type="text/css">
#oe_main_menu_navbar{{
  background-color: {main_menu_navbar_bg}
}}
</style>
            '''.format(
                main_menu_navbar_bg=r.main_menu_navbar_bg,
            )

            r.html = html

 
