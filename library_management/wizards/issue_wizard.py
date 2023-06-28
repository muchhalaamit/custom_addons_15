# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, timedelta


class IssueWizard(models.TransientModel):
    _name = "issue.wizard"
    _description = "Issue Wizard"

    # Wizard to cofirm the issue.bok
    def action_confirm(self):
        issue_book_record = self.env["issue.book"].search([("id", "=", self._context.get("active_id"))])
        issue_book_record.write({"state": "issued"})
        issue_book_record.issue_date = date.today()
        issue_book_record.submission_date = date.today() + timedelta(days=15)
        for line in issue_book_record.book_lines_ids:
            for _ in range(line.issue_quantity):
                register_id = [
                    {
                        "entry_id": self._context.get("active_id"),
                        "issued_date": issue_book_record.issue_date,
                        "issued_book_id": line.book_name_id.id,
                        "book_name": line.book_name_id.book_name,
                    }
                ]
                create_data = self.env["register.date"].create(register_id)
