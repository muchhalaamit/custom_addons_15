from odoo import fields, models, api, _
from datetime import datetime, date


class ReturnBook(models.TransientModel):
    _name = "return.book"
    _description = "Return Book wizard"

    return_book_ids = fields.One2many("register.data.lines", "relation_id", string="Select Books")

    # To return book
    def action_confirm(self):
        for rec in self:
            return_book_date = self.env["register.date"].search(
                [
                    ("entry_id", "=", self._context.get("active_id")),
                    ("returned_date", "=", False),
                    ("issued_book_id", "=", rec.return_book_ids.book_id.id),
                ]
            )
            for book_line in return_book_date:
                for book in range(rec.return_book_ids.return_quantity):
                    return_book_date[book].returned_date = date.today()
            # To change the state to return
            register_date_lines = self.env["register.date"].search([("entry_id", "=", self._context["active_id"])])
            for res in register_date_lines:
                date_list = []
                if res.returned_date:
                    date_list.append(True)
                else:
                    date_list.append(False)
            if all(date_list):
                self.env["issue.book"].search([("id", "=", self._context["active_id"])]).write({"state": "return"})


class RegisterDateLines(models.TransientModel):
    _name = "register.data.lines"
    _description = "Register Date Data"

    relation_id = fields.Many2one("return.book")
    book_id = fields.Many2one("book.details", string="Book ID")
    issued_quantity = fields.Integer("Issued Quantity", readonly=True)
    return_quantity = fields.Integer("Return Quantity")
    remaining_quantity = fields.Integer(string="Remaining Quantity")
