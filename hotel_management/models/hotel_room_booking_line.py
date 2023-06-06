# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import date


class HotelRoomBookingLine(models.Model):
    _name = "hotel.room.booking.line"
    _description = "Room Booking Line"
    _rec_name = "hotel_room"

    number_of_adults = fields.Integer(string="Number of Adults", default=1)
    number_of_children = fields.Integer(string="Number of Children", default=1)
    hotel_room = fields.Many2one("hotel.room", string="Hotel Room")
    price = fields.Float(string="Room Charge")
    hotel_room_booking_id = fields.Many2one("hotel.room.booking")

    # constrain for adult limit
    @api.constrains("number_of_adults")
    def check_adult_number(self):
        for rec in self:
            if rec.number_of_adults > 8 or rec.number_of_adults <= 0:
                raise ValidationError("The number of adults is more/less than limit 8.")
            elif rec.number_of_children > 6 and rec.number_of_children <= 0:
                raise ValidationError("The number of children is more than limit 6.")

    # Discount price if booking date is in date
    @api.onchange("hotel_room")
    def onchange_room_price(self):
        for rec in self:
            room_data = self.env["hotel.room"].search([("id", "=", rec.hotel_room.id)])
            print(room_data)
            if rec.hotel_room:
                if (
                    room_data.discount_valid_from
                    < date.today()
                    < room_data.discount_valid_till
                ):
                    rec.price = room_data.room_price - (
                        (room_data.room_price * room_data.room_discount) / 100
                    )
                else:
                    rec.price = rec.hotel_room.room_price
