# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class IssueBook(models.Model):
    _name = "issue.book"
    _inherit = "mail.thread"
    _rec_name = "user_name_id"

    user_name_id = fields.Many2one("res.partner", string="User Name", required=True)
    book_lines_ids = fields.One2many("register.books", "empty_field", string="Books")
    address = fields.Text(string="User Address")
    contact_no = fields.Char(string="User Contact No")
    email = fields.Char(string="User Email ID")
    issue_date = fields.Date(string="Issue Date", readonly=True)
    state = fields.Selection(
        selection=[("draft", "Draft"), ("issued", "Issued"), ("return", "Returned")],
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default="draft",
    )
    company_id = fields.Many2one(
        "res.company",
        store=True,
        copy=False,
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="company_id.currency_id",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    total_charge = fields.Monetary(string="Late fees", compute="_compute_late_fees")
    book_dropdwon = fields.Many2one("book.details", string="Book")
    quantity = fields.Integer(string="Quantity", default=1)
    submission_date = fields.Date(string="Submission Date")
    color = fields.Integer("Color", compute="_get_color")
    image = fields.Image(string="Image")

    def _get_color(self):
        for rec in self:
            if rec.state == "draft":
                rec.color = 4
            elif rec.state == "issued":
                rec.color = 1
            else:
                rec.color = 10

    # To fill fields of book code, book name and author name while selecting user
    @api.onchange("user_name_id")
    def _onchange_name_detail(self):
        for rec in self:
            rec.email = ""
            if rec.user_name_id:
                res_data = self.env["res.partner"].search(
                    [("id", "=", rec.user_name_id.id)]
                )
                rec.email = res_data.email
                rec.contact_no = res_data.phone
                rec.image = res_data.image_1920
                if not res_data.street2:
                    rec.address = (
                        str(res_data.street)
                        + "\n"
                        + str(res_data.zip)
                        + "\n"
                        + str(res_data.city)
                    )
                else:
                    rec.address = (
                        str(res_data.street)
                        + "\n"
                        + str(res_data.street2)
                        + "\n"
                        + str(res_data.zip)
                        + "\n"
                        + str(res_data.city)
                    )

    # Wizard on issue button
    def action_issue_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "issue.wizard",
            "name": _("Issue"),
            "view_mode": "form",
            "target": "new",
        }

    # Isuue Button calls wizard button
    def issue_book_view(self):
        return IssueBook.action_issue_wizard(self)

    # Return Button calls wizard
    def return_book_view(self):
        book_line_list = []
        for rec in self.book_lines_ids:
            book_line_list.append(
                (
                    0,
                    0,
                    {
                        "book_id": rec.book_name_id.id,
                        "issued_quantity": rec.issue_quantity,
                        "return_quantity": rec.non_return_quantity,
                        "remaining_quantity": rec.non_return_quantity,
                    },
                )
            )
        return {
            "type": "ir.actions.act_window",
            "name": "Return Book",
            "res_model": "return.book",
            "view_mode": "form",
            "target": "new",
            "context": {"default_return_book_ids": book_line_list},
        }

    # This is commented becaus ondelete="cascade" added in a field.
    # To unlink the data if data is deleted from issue.book
    # def unlink(self):
    #   for line in self.book_lines_ids:
    #       self.env["register.books"].search([("id", "=", line.id)]).unlink()
    #   return super(IssueBook, self).unlink()

    # search_read method to get email, contact and address
    @api.onchange("user_name_id")
    def _onchange_user_data(self):
        for rec in self:
            if rec.user_name_id:
                user_data = self.env["res.partner"].search_read(
                    [("id", "=", rec.user_name_id.id)],
                    [
                        "email",
                        "phone",
                        "street",
                        "street2",
                        "zip",
                        "city",
                        "image_1920",
                    ],
                    offset=0,
                    limit=100,
                )

    # Email sending by button
    def issue_book_email(self):
        template = self.env.ref("library_management.issue_book_mail_id")
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

    # Toal of late submission fees
    def _compute_late_fees(self):
        # value_list = []
        for rec in self:
            rec.total_charge = 0
            if rec.issue_date:
                single_charge = self.env["register.date"].search(
                    [("entry_id", "=", rec.id)]
                )
                for book in single_charge:
                    rec.total_charge += book.final_charge

    # To add book to book_line_ids
    def action_add_book(self):
        for line in self.book_lines_ids:
            self.env["register.books"].search(
                [("id", "=", line.id)]
            ).issue_book_data = line.id

        book_data = self.env["book.details"].search(
            [("id", "=", self.book_dropdwon.id)]
        )
        vals = {
            "book_name_id": self.book_dropdwon.id,
            "issue_quantity": self.quantity,
            "book_genre_ids": [(6, 0, book_data.book_type_ids.ids)],
        }
        if not self.book_lines_ids or self.book_lines_ids.book_name_id.ids:
            self.write({"book_lines_ids": [(0, 0, vals)]})
        else:
            for lines in self.book_lines_ids:
                register_book_data = self.env["register.books"].search(
                    [("id", "=", lines.id)]
                )
                if (
                    book_data.id == lines.book_name_id.id
                    and lines.id == register_book_data.issue_book_data
                ):
                    value_update = {
                        "issue_quantity": lines.issue_quantity + self.quantity,
                    }
                    self.write({"book_lines_ids": [(1, lines.id, value_update)]})
        self.book_dropdwon = None
        self.quantity = 1

    # Server action to send a retrn reminder mail
    def action_return_reminder(self):
        for rec in self:
            template = self.env.ref("library_management.return_reminder_mail").id
            template_id = self.env["mail.template"].browse(template)
            template_id.send_mail(rec.id, force_send=True)

    # Action scheduler for return book reminder
    def cron_return_reminder(self):
        all_data = self.env["issue.book"].search([])
        for rec in all_data:
            template = self.env.ref("library_management.return_reminder_mail").id
            template_id = self.env["mail.template"].browse(template)
            template_id.send_mail(rec.id, force_send=True)

    # constrain for not issuing same book multiple times
    @api.constrains("book_lines_ids")
    def check_book(self):
        for rec in self.book_lines_ids:
            if (
                self.env["register.books"].search_count(
                    [
                        ("book_name_id", "=", rec.book_name_id.id),
                        ("empty_field", "=", self.id),
                    ]
                )
                > 1
            ):
                raise ValidationError("Selected book is already added in the list.")

    # Constrain to check if same customer record is in draft state or not
    @api.constrains("user_name_id")
    def check_user_state(self):
        for rec in self:
            if (
                rec.search_count(
                    [
                        ("user_name_id", "=", rec.user_name_id.id),
                        ("state", "=", "draft"),
                    ]
                )
                > 1
            ):
                raise ValidationError("The user is already in draft state.")
