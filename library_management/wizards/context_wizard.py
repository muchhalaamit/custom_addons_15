# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ContextWizard(models.TransientModel):
    _name = "context.wizard"

    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")

    def action_confirm(self):
        book_type_nation = self.env["book.type"].search(
            [("id", "=", self._context.get("active_id"))]
        )
        book_type_nation.write(
            {
                "first_name": self.first_name,
                "middle_name": self.middle_name,
                "last_name": self.last_name,
            }
        )
