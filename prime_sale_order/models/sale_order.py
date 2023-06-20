# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
	_inherit = "sale.order"

	is_prime_sale = fields.Boolean(string="Prime Sale Order", default=False, copy=False)
