from odoo import fields,models


class BrandingObject(models.Model):
	_name = 'branding.object'
	_rec_name = 'branded_product_id'

	branded_product_id = fields.Many2one('product.product', string="Product",
			domain="[('is_branding', '=', True)]")
	comments = fields.Text(string="Comments")
	upload_logo = fields.Binary(string="Upload Logo")
	charges = fields.Selection(selection=[('fixed','Fixed'),('percentage','Percentage')], string="Charges")
	charges_cost = fields.Float(string="Charges Cost")
	sale_order_line_id = fields.Many2one('sale.order.line',string="Relation") 



