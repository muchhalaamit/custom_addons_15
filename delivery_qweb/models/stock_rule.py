from odoo import fields, models, api
import json


class StockRule(models.Model):
    _inherit = "stock.rule"

    # To get the data from sale_order_line and submit data to stock_picking
    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
    ):
        move_values = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )

        if values.get("sale_line_id"):
            sale_order_line = self.env["sale.order.line"].browse(
                values.get("sale_line_id")
            )
            # move_values['unit_price'] = sale_order_line.price_unit
            # move_values['sale_subtotal'] = sale_order_line.price_subtotal
            # move_values['sale_taxes'] = sale_order_line.tax_id
            move_values.update(
                {
                    "sale_taxes": sale_order_line.tax_id,
                    "sale_subtotal": sale_order_line.price_subtotal,
                    "unit_price": sale_order_line.price_unit,
                }
            )

        return move_values
