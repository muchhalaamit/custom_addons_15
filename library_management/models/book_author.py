# -*- coding: utf-8 -*-
from odoo import fields, models, api


class BookAuthor(models.Model):
    _name = "book.author"
    _description = "Book Author"
    _rec_name = "author_name"

    author_name = fields.Char(string="Author Name")
    email = fields.Char(string="Email id")
    contact_number = fields.Char(string="Contact Number")
    country = fields.Many2one("res.country", string="Country")
    address = fields.Text(string="Full Address")
    state = fields.Many2one("res.country.state", string="State", store=True)

    @api.onchange("country")
    def set_values_to(self):
        if self.country:
            ids = self.env["res.country.state"].search([("country_id", "=", self.country.id)])
            return {"domain": {"state": [("id", "in", ids.ids)]}}


class ResPartner(models.Model):
    _inherit = "res.partner"

    # new field to inherit res_partner and choosing if he/she is author or not
    is_author = fields.Boolean(string="Is Author")
