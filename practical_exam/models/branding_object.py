from odoo import fields, models


class BrandingObject(models.Model):
    _name = "branding.object"
    _rec_name = "branded_product_id"

    branded_product_id = fields.Many2one(
        "product.product", string="Product", domain="[('is_branding', '=', True)]"
    )
    comments = fields.Text(string="Comments")
    brand_image = fields.Binary(string="Brand Logo")
    charges_type = fields.Selection(
        selection=[("fixed", "Fixed"), ("percentage", "Percentage")],
        string="Charges Type",
    )
    charges_cost = fields.Float(
        string="Charges Cost", domain="[('charges', '==', 'percentage')]"
    )
    sale_order_line_id = fields.Many2one("sale.order.line", string="Relation")
