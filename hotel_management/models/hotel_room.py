# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.osv import expression


class HotelRoom(models.Model):
    _name = "hotel.room"
    _description = "Hotel Room"
    _rec_name = "room_code"

    room_code = fields.Char(string="Room Code", readonly=True)
    number_of_subrooms = fields.Integer(string="Number of Subroom")
    hotel_id = fields.Many2one("hotel.details", string="Hotel")
    room_type = fields.Selection(
        selection=[("ac", "AC Room"), ("non_ac", "Non-AC Room")], string="Room Type"
    )
    room_discount = fields.Float(string="Discount(%)")
    discount_valid_from = fields.Date(string="Valid from")
    discount_valid_till = fields.Date(string="Valid till")
    room_price = fields.Integer(string="Room Price")

    # To create the sequence for room
    @api.model
    def create(self, vals):
        if not vals.get("room_code"):
            seq = self.env["ir.sequence"].next_by_code("hotel.room")
            vals["room_code"] = seq[0:4] + seq[4:]
        return super(HotelRoom, self).create(vals)

    # hotelname/roomcode
    def name_get(self):
        result = []
        for rec in self:
            name = rec.hotel_id.hotel_name + "/" + rec.room_code
            result.append((rec.id, name))
        return result

    # To showo only selected hotel's rooms
    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if self.env.context.get("record"):
            args = expression.AND(
                [[("hotel_id", "=", self._context.get("record"))], args]
            )
        return super(HotelRoom, self)._name_search(
            name, args, limit=limit, name_get_uid=None
        )
