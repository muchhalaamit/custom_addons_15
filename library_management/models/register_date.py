# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, timedelta


class RegisterDate(models.Model):
    _name = "register.date"
    _rec_name = "book_name"

    entry_id = fields.Integer(string="Entry Id")
    issued_book_id = fields.Integer(string="Book ID")
    book_name = fields.Char(string="Book")
    book_charges = fields.Integer(string="Charges", compute="_compute_book_charges")
    issued_date = fields.Date(string="Isuue Date")
    returned_date = fields.Date(string="Return Date")
    deadline_date = fields.Date(
        string="Last Date to Return", compute="_compute_deadline_date"
    )
    final_charge = fields.Integer(string="Final Charges")

    # Deadline date
    def _compute_deadline_date(self):
        for rec in self:
            if rec.issued_date:
                rec.deadline_date = rec.issued_date + timedelta(days=15)
            else:
                rec.deadline_date = False

    # Book Charges Calculation
    def _compute_book_charges(self):
        self.book_charges = 0
        for rec in self:
            issued_book_charge = (
                self.env["book.details"]
                .search([("book_name", "=", rec.book_name)])
                .book_delay_charges
            )
            if not rec.returned_date and str(date.today()) > str(rec.deadline_date):
                rec.book_charges += issued_book_charge + (
                    issued_book_charge * (date.today() - rec.deadline_date).days // 5
                )
                rec.final_charge = rec.book_charges
