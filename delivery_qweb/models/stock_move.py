from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    unit_price = fields.Float(string="Unit Price")
    sale_taxes = fields.Many2many("account.tax", string="Taxes", store=True)
    sale_subtotal = fields.Float(string="Sub Total")


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # Adding data to report
    def _get_aggregated_product_quantities(self, **kwargs):
        res = super(StockMoveLine, self)._get_aggregated_product_quantities()
        for rec in self:
            for key in res.keys():
                if res[key]["product"] == rec.product_id:
                    res[key]["unit"] = rec.move_id.unit_price
                    res[key]["taxes"] = rec.move_id.sale_taxes.name
                    res[key]["subtotal"] = rec.move_id.sale_subtotal
        return res
