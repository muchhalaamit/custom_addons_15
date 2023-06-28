from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_image = fields.Binary(string="Product Image", related="product_id.image_1920")

    # @api.onchange('product_id')
    # def product_id_change(self):
    # 	res = super(SaleOrderLine, self).product_id_change()
    # 	for rec in self:
    # 		if rec.product_id:
    # 			rec.product_image = rec.product_id.image_1920
    # 	return super(SaleOrderLine,self).product_id_change()
