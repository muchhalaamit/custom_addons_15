from odoo import fields, models, api


class StockMoveLines(models.Model):
    _inherit = "stock.move.line"

    sale_price_subtotal = fields.Float(string="Sub Total")

    def _get_aggregated_product_quantities(self, **kwargs):
        res = super(StockMoveLines, self)._get_aggregated_product_quantities()
        sale_order_data = self.env["sale.order"].search([("picking_ids", "=", self.picking_id.id)])
        sale_total_price = sale_order_data.tax_totals_json
        for product in sale_order_data.order_line:
            res["sub_total_price"] = product.price_subtotal
        return res
