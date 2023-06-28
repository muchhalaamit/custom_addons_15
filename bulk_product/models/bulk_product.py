from odoo import fields, models, api


class BulkProduct(models.Model):
    _name = "bulk.product"

    name = fields.Char(string="Name")
    product_name_ids = fields.Many2many("product.product", string="Product_name")


class ProductDetails(models.Model):
    _inherit = "product.template"

    product_desc_show = fields.Boolean(string="product_Description_Show")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    service_id = fields.Many2one("bulk.product", string="Product Template")

    # To add lines in sale_order_lines when template is selected
    @api.onchange("service_id")
    def _onchange_service_id(self):
        for rec in self:
            rec.order_line = False
            if rec.service_id != False:
                order_line_data = self.env["sale.order.line"]
                template_data = self.env["bulk.product"].search([("id", "=", rec.service_id.id)])
                for line in template_data.product_name_ids:
                    vals = {
                        "order_id": self.id,
                        "product_id": line.id,
                    }
                    order_line_data.new(vals).product_id_change()
                    order_line_data.write(vals)

    # To add the lines in the wizard whe server action is called
    def server_action_split_delivery(self):
        product_id_list = []
        for rec in self.order_line:
            product_id_list.append((0, 0, {"product_product_id": rec.product_id.id}))
        return {
            "type": "ir.actions.act_window",
            "res_model": "split.delivery",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_line_ids": product_id_list,
                "reference_id": self.id,
            },
        }
