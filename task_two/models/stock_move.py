from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    other_info = fields.Char(string="Other Information")
