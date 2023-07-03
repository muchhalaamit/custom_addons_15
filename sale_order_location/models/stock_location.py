# -*- coding: utf-8 -*-

from odoo import models


class Location(models.Model):
	_inherit = "stock.location"

	# def name_get(self):
	# 	"""This method will show the location of selected roduct with available quantity."""
	# 	result = []
	# 	for rec in self:
	# 		product_id = self._context.get("product_id")
	# 		available_qty = self.env["stock.quant"].search_count([("location_id", "=", rec.id), ("product_id", "=", product_id)])
	# 		name_qty = rec.name + " - " + str(available_qty)
	# 		result.append((rec.id, name_qty))
	# 	return result

	def name_get(self):
		result = []
		for rec in self:
			product_id = self._context.get("product_id")
			location_data = self.env["stock.quant"].search([("product_id", "=", product_id)])
			if location_data:
				for quant in location_data[0]:
					name = f"{quant.location_id.name} - {quant.quantity}"
					result.append((rec.id, name))
			else:
				name = rec.name
				result.append((rec.id, name))
		return result

	# def name_get(self):
	# 	"""This method will show the location of selected roduct with available quantity."""
	# 	result = []
	# 	for rec in self:
	# 		product_id = self._context.get("product_id")
	# 		location_data = self.env["stock.quant"].search([("product_id", "=", product_id)])
	# 		name_qty = f"{rec.name} - {location_data[0].available_quantity}"
	# 		result.append((rec.id, rec.name))
	# 	return result