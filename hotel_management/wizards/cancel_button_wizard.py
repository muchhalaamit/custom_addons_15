# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, timedelta


class CancelWizard(models.TransientModel):
    _name = "cancel.wizard"

    select_cancel = fields.Selection(
        selection=[
            ("cancel", "Cancel Booking"),
            ("cancel_mail", "Cancel Booking and Send Mail")], string="Cancel Room")

    # Wizard to cofirm the issue.bok
    def action_confirm(self):
        booking_detail = self.env["hotel.room.booking"].search([("id", "=", self._context.get("active_id"))])
        booking_detail.write({"state": "cancel"})
        if self.select_cancel == "cancel_mail":
            template = self.env.ref("hotel_management.booking_cancel_mail_id").id
            template_id = self.env["mail.template"].browse(template)
            template_id.send_mail(self._context.get("active_id"), force_send=True)
