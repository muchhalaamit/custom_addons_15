# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def compute_branding_cost(self):
        """This method will add branding lines of selected product to the sale order line. And
        also update unit price of branding lines accordingly."""
        for rec in self.order_line:
            if rec.branding_object_ids.charges_type == "percentage":
                rec.branding_object_ids.charges_costing = (
                    rec.price_unit * rec.branding_object_ids.charges_costing
                ) / 100
                rec.price_unit = (
                    rec.price_unit + rec.branding_object_ids.charges_costing
                )

    def reset_lines(self):
        """This method will remove all branding lines from the sale order line."""
        pass


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    branding_object_ids = fields.One2many(
        "branding.object", "sale_order_line_id", string="Brand Object"
    )
