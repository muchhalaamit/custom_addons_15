# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
	_inherit = "sale.order"

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
