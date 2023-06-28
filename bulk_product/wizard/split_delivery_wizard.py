from odoo import fields, models, api, _


class SplitDelivery(models.TransientModel):
    _name = "split.delivery"

    user_id = fields.Many2one("res.partner", string="User Name")
    product_line_ids = fields.One2many("split.product.line", "ref_id", string="Products")

    # To cancel the record when the split method is called and create new record
    def action_confirm(self):
        delivery_data = self.env["stock.picking"].search([("sale_id", "=", self._context.get("reference_id"))])
        for rec in delivery_data:
            new_delivery_record = rec.copy()
            new_delivery_record.action_confirm()
            rec.action_cancel()
            # self.env["stock.move.line"].create


class SplitProductLine(models.TransientModel):
    _name = "split.product.line"

    ref_id = fields.Many2one("split.delivery", string="Reference")
    product_product_id = fields.Many2one("product.product", string="Product")
    split_choice = fields.Boolean(string="Tick")
