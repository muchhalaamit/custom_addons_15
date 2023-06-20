# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
	_inherit = "sale.order"

	shipping_hold = fields.Boolean(string="Shipping Hold", default=False, copy=False)

	@api.onchange("shipping_hold")
	def _onchange_shipping_hold(self):
		stock_picking = self.env["stock.picking"].browse(self.picking_ids._origin.ids)
		if stock_picking:
			pickings = stock_picking.filtered(lambda picking: picking.state not in "done" and picking.picking_type_code == 'outgoing')
			pickings.shipping_hold = self.shipping_hold

