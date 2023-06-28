# -*- coding: utf-8 -*-

import json

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
	_inherit = "sale.order"

	sale_order_total = fields.Char(string="Sale Order Total", compute="_compute_total")
	available_prime = fields.Integer()
	is_prime_sale = fields.Boolean(
		string="Prime Sale Order",
		default=False,
		copy=False,
		tracking=True,
		readonly=True,
		help="Tick this boolean to make this sale order prime.",
	)

	# To return the label of current state
	def get_current_state_label(self):
		current_state = dict(self._fields["state"].selection).get(self.state)
		return current_state

	# Method to set prime sale order
	def set_prime_sale(self):
		if self.state in ("draft", "sent"):
			self.is_prime_sale = True
		else:
			raise ValidationError(
				f"This order can't be a prime sale order as it is in '{self.get_current_state_label()}' state."
			)

	# Method to clear prime_sale_order
	def clear_prime_sale(self):
		state = self.get_current_state_label()
		if self.state in ("draft", "sent"):
			self.is_prime_sale = False
		else:
			raise ValidationError(
				f"This action can't be done as it is in '{self.get_current_state_label()}' state."
			)

	# Smart button to show if the order is prime or not
	def prime_sale(self):
		for rec in self:
			rec.available_prime = self.search_count([("is_prime_sale", "=", True)])

	# To copy the current record
	def copy_current_record(self):
		if self.is_prime_sale:
			raise ValidationError("This record is prime. It can't be copied.")
		else:
			self.copy()

	# context pass in write method
	def write(self, values):
		ctx = dict(self._context)
		ctx.update({"write_context": "passed"})
		self = self.with_context(ctx)
		res = super(SaleOrder, self).write(values)
		return res

	# passing the context when the action_confirm is called and stock_picking is created
	def action_confirm(self):
		ctx = dict(self._context)
		ctx.update({"current_model": "sale"})
		self = self.with_context(ctx)
		res = super(SaleOrder, self).action_confirm()
		return res

	# Method for random button
	def random_button(self):
		current_user = self.user_id.id
		print(self.read())
		sale_orders = self.env["sale.order"].search([("user_id", "=", current_user)])

	# A method for compute field sale_order_total
	def _compute_total(self):
		for rec in self:
			rec.sale_order_total = json.loads(rec.tax_totals_json)["amount_total"]