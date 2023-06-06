from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.template"

    is_branding = fields.Boolean(string="Is Branding")
