# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BrandingObject(models.Model):
    _name = "branding.object"
    _description = "Branding Object"
    _rec_name = "product_name_id"

    product_name_id = fields.Many2one(
        "product.product", string="Products", domain="[('is_branding', '=', True)]")
    comments = fields.Char(string="Comments", required=True)
    product_image = fields.Image(string="Product Image")
    charges_type = fields.Selection(
        selection=[("fixed", "Fixed"), ("percentage", "Percentage")],
        string="Charges Type",
    )
    charges_costing = fields.Float(string="Charge Costing(%)")
    sale_order_line_id = fields.Many2one("sale.order.line", string="Brand")
    anything = fields.Char(string="Anything")

    @api.constrains("charges_costing")
    def _check_charge_costing(self):
        """This fuction will check if the entered value is between 0 and 100 or it will
        show a va;idation error."""
        for rec in self:
            if rec.charges_costing < 0 or rec.charges_costing > 100:
                raise ValidationError("The discount entered is invalid.")
