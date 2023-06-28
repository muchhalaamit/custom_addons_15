# -*- coding: utf-8 -*-

import json
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Picking(models.Model):
	_inherit = "stock.picking"

	total_sale_order = fields.Char(string="Total", compute="_compute_total_sale_order")
	# A boolean is added for the picking created from a sale_order.
	is_sale_order = fields.Boolean(string="Is sale picking", default=False, readonly=True)

	# When stock_picking is created, context is verified and the booland is set to True.
	@api.model
	def create(self, vals):
		res = super(Picking, self).create(vals)
		if "current_model" in res._context:
			res.is_sale_order = True
		return res

	# Compute field and method to show the total of sale order
	def _compute_total_sale_order(self):
		for rec in self:
			if rec.sale_id:
				rec.total_sale_order = json.loads(rec.sale_id.tax_totals_json)["amount_total"]
			else:
				rec.total_sale_order = "No Total is available"