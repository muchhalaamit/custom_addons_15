# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        for rec in res.order_line:
            if rec.product_id.sale_limit == 0 and rec.product_uom_qty:
                raise ValidationError(f"Quantity of {rec.product_id.name} is zero and entered {rec.product_uom_qty}."
                                      f"Kindly Check the quantity.")
            elif 0 < rec.product_id.sale_limit < rec.product_uom_qty:
                rec.product_uom_qty = rec.product_id.sale_limit
        return res
