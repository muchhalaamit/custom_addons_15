from odoo import models


class StockRule(models.Model):
    """In this method, the data of sale_order_line is added to dictionary which is passed to delivery"""

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
            move_values.update({"other_info": sale_order_line.other_information})
        return move_values
