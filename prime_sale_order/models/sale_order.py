# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
	_inherit = "sale.order"

	is_prime_sale = fields.Boolean(string="Prime Sale Order",
			default=False,
			copy=False,
			tracking=True,
			readonly=True,
			help="To create a prime sale order")

	def set_prime_sale(self):
		print("\n\n\n", dict(self._fields.state.items()))

		if self.state in ('draft', 'sent'):
			self.is_prime_sale = True
		else:
			raise ValidationError(f"This order can't be a prime sale order as it is in '{self.state}' state.")

	def clear_prime_sale(self):
		if self.state in ('draft', 'sent'):
			self.is_prime_sale = False
		else:
			raise ValidationError(f"This action can't be done as it is in '{self.state}' state.")
