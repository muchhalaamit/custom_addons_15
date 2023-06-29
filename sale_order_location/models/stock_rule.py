# -*- coding: utf-8 -*-

from odoo import models


class StockRule(models.Model):
	_inherit = "stock.rule"

	# To get the data of location from sale_order_line and add to stock_picking
	def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values,):
		move_values = super()._get_stock_move_values(
			product_id, product_qty, product_uom, location_id, name, origin, company_id, values,)
		if values.get("sale_line_id"):
			sale_order_line = self.env["sale.order.line"].browse(values.get("sale_line_id"))
			move_values.update({"location_id": sale_order_line.product_location_id.id,})
		return move_values
