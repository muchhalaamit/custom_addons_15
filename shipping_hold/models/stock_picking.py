# -*- coding: utf-8 -*-

from odoo import fields, models


class Picking(models.Model):
	_inherit = "stock.picking"

	shipping_hold = fields.Boolean(string="Shipping Hold", default=False, copy=False)