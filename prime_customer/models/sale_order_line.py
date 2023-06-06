from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        for rec in self:
            if rec.product_id and rec.order_id.partner_id.is_prime_customer:
                rec.discount = rec.order_id.partner_id.prime_discount
        return res
