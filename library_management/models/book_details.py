# -*- coding: utf-8 -*-
from odoo import fields, models, api
import datetime


class BookDetails(models.Model):
    _name = "book.details"
    _rec_name = "book_name"

    book_id = fields.Char(string="Book Id", readonly=True)
    image = fields.Image(string="Image", max_width=64, max_height=64)
    book_name = fields.Char(string="Book Name", ondelete="restrict")
    book_price = fields.Float(string="Price ₹")
    book_pages = fields.Integer(string="Total Pages")
    book_author_id = fields.Many2one(
        "book.author", string="Author", ondelete="restrict"
    )
    book_quantity = fields.Integer(string="Book Quantity")
    book_code = fields.Char(string="Book Code")
    available_books = fields.Integer(
        string="Available Book", compute="_compute_book_quantity"
    )
    book_type_ids = fields.Many2many("book.type", string="Type")
    book_delay_charges = fields.Integer(string="Delay Charge", default=10)

    @api.model
    def create(self, vals):
        if not vals.get("book_id"):
            seq = self.env["ir.sequence"].next_by_code("book.details")
            vals["book_id"] = (
                seq[0:4]
                + "/"
                + datetime.date.today().strftime("%b").upper()
                + "/"
                + seq[4:]
            )
        return super(BookDetails, self).create(vals)

    def name_get(self):
        result = []
        for rec in self:
            name = (
                rec.book_code
                + " - "
                + rec.book_name
                + " - "
                + rec.book_author_id.author_name
            )
            result.append((rec.id, name))
        return result

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if name:
            args = [
            "|", "|", ("book_name", operator, name), ("book_author_id", operator, name), ("book_id", operator, name),
            ] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def action_button_count(self):
        pass

    def _compute_book_quantity(self):
        for rec in self:
            issued_quantity = self.env["register.date"].search_count(
                [("issued_book_id", "=", rec.id), ("returned_date", "=", False)]
            )
            rec.available_books = rec.book_quantity - issued_quantity
