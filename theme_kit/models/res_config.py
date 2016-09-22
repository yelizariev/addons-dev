# -*- coding: utf-8 -*-
import hashlib

from openerp import models, fields, api

FIELD_PARAM_LIST = [
    ('theme_id', 'theme_kit.current_theme_id'),
    ('favicon_id', 'theme_kit.current_favicon_id'),
]

CUSTOM_CSS_ARCH = '''<?xml version="1.0"?>
<t t-name="theme_kit.custom_css">
%s
</t>
'''


class Config(models.Model):

    _name = 'theme_kit.config'
    _inherit = 'res.config.settings'

    theme_id = fields.Many2one('theme_kit.theme', string="Color Scheme")
    favicon_id = fields.Many2one('ir.attachment', string="Favicon")

    @api.multi
    def get_default_ids(self):
        res = {}
        for field, param in FIELD_PARAM_LIST:
            value = self.env['ir.config_parameter'].get_param(param)
            try:
                res[field] = int(value)
            except:
                pass
        return res

    @api.multi
    def set_ids(self):
        for field, param in FIELD_PARAM_LIST:
            self.env['ir.config_parameter'].set_param(param, getattr(self, field).id or '')

    @api.multi
    def set_theme(self):
        custom_css = self.env.ref('theme_kit.custom_css')
        code = ''
        if self.theme_id:
            code = self.theme_id.code
        arch = CUSTOM_CSS_ARCH % code
        custom_css.write({'arch': arch})

    def _attachment2url(self, att):
        sha = hashlib.sha1(getattr(att, '__last_update')).hexdigest()[0:7]
        return '/web/image/%s-%s' % (att.id, sha)

    @api.multi
    def set_favicon(self):
        url = ''
        if self.favicon_id:
            url = self.favicon_id.url or self._attachment2url(self.favicon_id)
        self.env['ir.config_parameter'].set_param('web_debranding.favicon_url', url)


