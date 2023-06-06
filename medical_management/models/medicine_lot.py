# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MedicineLot(models.Model):
    _name = "medicine.lot"

    lot = fields.Char(string="Lot No.", readonly=True)
    name_id = fields.Many2one("medicine.information", string="Medicine Name")
    manufacturing = fields.Date(string="Manufacturing Date")
    expiry = fields.Date(string="Expiry Date")
    quantity = fields.Integer(string="Quantity")
    state = fields.Selection(
        selection=[("draft", "Not Expired"), ("done", "Expired")],
        string="Status",
        required=True,
        readonly=True,
        default="draft",
    )

    # create method for medicine lot number
    @api.model
    def create(self, vals):
        if not vals.get("lot"):
            seq_lot = self.env["ir.sequence"].next_by_code("medicine.lot")
            vals["lot"] = seq_lot
        return super(MedicineLot, self).create(vals)
