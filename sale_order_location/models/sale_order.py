# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
	_inherit = "sale.order"

	confirm_proceed = fields.Boolean(default=False)

	def confirm_stock_proceed(self):
		"""A custom button added to raise a validation if location is empty and
		to get access of Confirm button."""
		for rec in self.order_line:
			# stock_quant_data = self.env["stock.quant"].search([("product_id", "=", rec.product_id.id)]).mapped("location_id")
			# for i in stock_quant_data:
			# 		print("\n\n\n", i.name, "----", i.quant_ids.available_quantity)
			if rec.product_location_id.id == False:
				raise ValidationError("The location is not selected. Please select the location.")
			else:		
				self.confirm_proceed = True


class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	product_location_id = fields.Many2one("stock.location", string="Location")

	@api.onchange('product_id')
	def _onchange_product_location(self):
		"""This onchange method will show only selected product's locations."""
		if self.product_id:
			stock_quant_data = self.env["stock.quant"].search([("product_id", "=", self.product_id.id)]).mapped("location_id")
			return {"domain": {"product_location_id": [("id", "in", stock_quant_data.ids)]}}
