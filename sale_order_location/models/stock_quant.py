# -*- coding: utf-8 -*-

from odoo import models


class StockQuant(models.Model):
	_inherit = "stock.quant"

	def name_get(self):
		"""This method will show the location of selected roduct with available quantity."""
		result = []
		for rec in self:
			name = (rec.name + " - " + rec.available_quantity)
			result.append((rec.id, name))
		return result