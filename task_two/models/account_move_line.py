from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    other_information = fields.Char(string="Other Information")
