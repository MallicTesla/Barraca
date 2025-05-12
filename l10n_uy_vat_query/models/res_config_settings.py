# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_server_url = fields.Char(string="URL del servidor API", related='company_id.api_server_url', readonly=False)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.company_id.write({'api_server_url': self.api_server_url})


    def write(self, vals):
        res = super(ResConfigSettings, self).write(vals)
        if 'api_server_url' in vals:
            self.company_id.api_server_url = self.api_server_url
        return res
