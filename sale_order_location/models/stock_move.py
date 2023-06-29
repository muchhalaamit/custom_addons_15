# -*- coding: utf-8 -*-

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    location_id = fields.Many2one("stock.location", string="Location")
