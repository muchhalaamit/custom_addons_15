from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def compute_branding_cost(self):
        """method to add sale_order_lines if preesed 'Compute Branding Cost' button"""
        for rec in self:
            if rec.order_line:
                branding_records = self.env["branding.object"].search(
                    [("sale_order_line_id", "=", rec.order_line.ids)]
                )
                for record in branding_records:
                    if record.branded_product_id:
                        if record.charges_type == "fixed":
                            vals = {
                                "product_id": record.branded_product_id.id,
                                "product_uom_qty": record.sale_order_line_id.product_uom_qty,
                                "price_unit": record.charges_cost,
                                "branding_status": True,
                            }
                        elif record.charges_type == "percentage":
                            vals = {
                                "product_uom_qty": record.sale_order_line_id.product_uom_qty,
                                "product_id": record.branded_product_id.id,
                                "price_unit": record.sale_order_line_id.price_unit
                                * (record.charges_cost / 100),
                                "branding_status": True,
                            }
                        self.write({"order_line": [(0, 0, vals)]})

    def branding_reset(self):
        """method to delete sale_order_lines if created"""
        for rec in self.order_line:
            if rec.branding_status:
                rec.unlink()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    branding_product_ids = fields.One2many(
        "branding.object", "sale_order_line_id", string="Product"
    )
    branding_status = fields.Boolean(string="Brand")
