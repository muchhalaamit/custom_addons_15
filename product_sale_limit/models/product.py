# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    sale_limit = fields.Integer(string="Sale Limit")
