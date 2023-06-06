from odoo import fields, models, api


class ProductDetails(models.Model):
    _name = "product.details"

    name = fields.Char(string="Name")
