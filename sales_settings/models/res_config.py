# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _description = "Sale Cofiguration Settings"

    discount_limit = fields.Boolean(string="Discount Limit")
    product_description = fields.Char(string="Description")
    res_partner_id = fields.Many2one("res.partner", string="Partner")

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "sales_settings.discount_limit", self.discount_limit
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "sales_settings.product_description", self.product_description
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "sales_settings.res_partner_id", self.res_partner_id.id
        )
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        setting_values = self.env["ir.config_parameter"].sudo()
        res.update(
            discount_limit=setting_values.get_param("sales_settings.discount_limit"),
            product_description=setting_values.get_param(
                "sales_settings.product_description"
            ),
            res_partner_id=int(
                setting_values.get_param("sales_settings.res_partner_id")
            ),
        )
        return res
