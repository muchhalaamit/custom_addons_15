# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class HotelDetails(models.Model):
    _name = "hotel.details"
    _description = "Hotel Details"
    _rec_name = "hotel_name"

    hotel_image = fields.Image(string="Image")
    hotel_name = fields.Char(string="Hotel")
    hotel_address = fields.Text(string="Address")
    hotel_contact = fields.Char(string="Contact No")
    hotel_website = fields.Char(string="Website")
    hotel_email = fields.Char(string="Customer Support")
    product_id = fields.Many2one("product.product")


# Inheritancs of product and sale_order
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    product_one = fields.Char(string="Product Reference 1")
    product_two = fields.Char(string="Product reference 2")

    @api.onchange("product_id")
    def product_id_change(self):
        for rec in self.product_id:
            model_rec = self.env["product.product"].search([("id", "=", rec.id)])
            for record in model_rec:
                self.product_one = record.pro_one
                self.product_two = record.pro_two
        # for rec in model_rec:
        return super(SaleOrderLine, self).product_id_change()


class ProductProduct(models.Model):
    _inherit = "product.template"

    pro_one = fields.Char(string="Product ref1")
    pro_two = fields.Char(string="Product ref2")
    description_show = fields.Boolean(string="Discription Show")


# Server action to merge quatation
class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
            ("extra", "Extra"),
        ], string="Status", readonly=True, copy=False, index=True, tracking=3, default="draft")

    def action_confirm(self):
        res = super().action_confirm()
        self.state = "extra"
        return res

        # Server action to send a retrn reminder mail

    def action_merge_quotation(self):
        if len(self.partner_id.ids) == 1 and all(rec.state == "draft" for rec in self):
            self.action_cancel()
            new_rcord = self.create({"partner_id": self.partner_id.ids[0],})
            for lines in self.order_line:
                lines.copy({"order_id": new_rcord.id})
            new_rcord.action_confirm()
        else:
            raise ValidationError("Selected records are having different partners or the state is not quotation.")
