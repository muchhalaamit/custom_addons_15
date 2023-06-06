from odoo import fields, models, api
import json


class StockPicking(models.Model):
    _inherit = "stock.picking"

    total_price = fields.Float(string="Total", compute="_compute_total_price")

    # Total assigning to delivery
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.sale_id.amount_total
