# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError


class RegisterBooks(models.Model):
    _name = "register.books"
    _rec_name = "book_name_id"

    book_name_id = fields.Many2one("book.details", string="Book")
    empty_field = fields.Many2one("issue.book", ondelete="cascade")
    issue_quantity = fields.Integer(string="Quantity", default=1)
    non_return_quantity = fields.Integer(
        string="Remaining Quantity", compute="_compute_remaining_quantity"
    )
    book_genre_ids = fields.Many2many("book.type", string="Book Genre")
    issue_book_data = fields.Integer(string="Issue Book ID")

    # To autofill the type of the book when book is selected
    @api.onchange("book_name_id")
    def onchange_book_type(self):
        for rec in self:
            book_type_search = self.env["book.details"].search(
                [("id", "=", self.book_name_id.id)]
            )
            for record in book_type_search:
                rec.update({"book_genre_ids": [(6, 0, record.book_type_ids.ids)]})

    def _compute_remaining_quantity(self):
        for rec in self:
            rec.non_return_quantity = 0
            rec.non_return_quantity = self.env["register.date"].search_count(
                [
                    ("entry_id", "=", rec.empty_field.id),
                    ("issued_book_id", "=", rec.book_name_id.id),
                    ("returned_date", "=", False),
                ]
            )
