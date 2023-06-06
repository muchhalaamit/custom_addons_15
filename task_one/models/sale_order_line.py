from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    ref = fields.Char(string="Product Reference")

    @api.onchange("product_id")
    def product_id_change(self):
        for rec in self:
            rec.ref = rec.product_id.default_code
        return super(SaleOrderLine, self).product_id_change()
