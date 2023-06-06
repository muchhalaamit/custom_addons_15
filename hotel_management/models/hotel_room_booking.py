# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from datetime import datetime
from odoo.exceptions import ValidationError


class HotelRoomBooking(models.Model):
    _name = "hotel.room.booking"
    _description = "Hotel Room"
    _rec_name = "hotel_name_id"

    hotel_name_id = fields.Many2one("hotel.details", string="Hotel")
    customer_name_id = fields.Many2one(
        "res.partner", string="Customer Name", required=True
    )
    customer_contact = fields.Char(string="Contact No")
    customer_address = fields.Text(string="Address")
    check_in_datetime = fields.Datetime(string="Check-in date & time", required=True)
    check_out_datetime = fields.Datetime(string="Check-out date & time", required=True)
    state = fields.Selection(
        selection=[("draft", "Draft"), ("booked", "Booked"), ("cancel", "Cancel")],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default="draft",
    )
    hotel_room_booking_line_ids = fields.One2many(
        "hotel.room.booking.line", "hotel_room_booking_id", string="Line"
    )

    # To fill fields of book code, book name and author name while selecting user
    @api.onchange("customer_name_id")
    def _onchange_name_detail(self):
        for rec in self:
            if rec.customer_name_id:
                res_data = self.env["res.partner"].search(
                    [("id", "=", rec.customer_name_id.id)]
                )
                rec.customer_contact = res_data.phone
                if not res_data.street2:
                    rec.customer_address = (
                        str(res_data.street)
                        + "\n"
                        + str(res_data.zip)
                        + "\n"
                        + str(res_data.city)
                    )
                else:
                    rec.customer_address = (
                        str(res_data.street)
                        + "\n"
                        + str(res_data.street2)
                        + "\n"
                        + str(res_data.zip)
                        + "\n"
                        + str(res_data.city)
                    )

    # button to cancle the room
    def hotel_room_cancel(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "cancel.wizard",
            "name": _("Cancel Room"),
            "view_mode": "form",
            "target": "new",
        }

    # button to book the room
    def hotel_room_book(self):
        for rec in self:
            rec.write({"state": "booked"})
            template = self.env.ref("hotel_management.room_booking_mail_id").id
            template_id = self.env["mail.template"].browse(template)
            template_id.send_mail(rec.id, force_send=True)

    # Send mail on button click
    def room_booking_mail(self):
        template = self.env.ref("hotel_management.room_booking_mail_id")
        template_id = self.env["mail.template"].browse(template.id)
        ctx = dict(default_template_id=template and template.id)
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    # Scheduler to send mail one hour before checkout
    def cron_chechout_reminder(self):
        all_data = self.env["hotel.room.booking"].search([])
        for rec in all_data:
            if (
                rec.check_out_datetime > datetime.now()
                and rec.state == "booked"
                and rec.check_out_datetime.hour - datetime.now().hour == 1
            ):
                template = self.env.ref("hotel_management.checkout_reminder_mail_id").id
                template_id = self.env["mail.template"].browse(template)
                template_id.send_mail(rec.id, force_send=True)

    # To check if every detail is correct or not
    @api.constrains("customer_name_id")
    def check_every_details(self):
        for rec in self:
            if (
                rec.check_in_datetime < datetime.now()
                and rec.check_out_datetime <= datetime.now()
            ):
                raise ValidationError("Entered date and time is invalid.")
