# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class BookType(models.Model):
    _name = "book.type"

    name = fields.Char(string="Book Genre")
    nation_select = fields.Selection(
        selection=[("india", "India"), ("pakistan", "Pakistan")], string="Nation"
    )

    # _sql_constraints = [
    #         ('code_name', 'unique (name)', 'Book name must be unique !')
    #     ]

    # When the rcord is duplicated, it should show name - number
    def copy(self, default=None):
        if default is None:
            default = {}
        default["name"] = self._get_copy_name()
        return super(BookType, self).copy(default)

    def _get_copy_name(self):
        parts = self.name.split(" - ")
        name = parts[0]
        if len(parts) > 1:
            number = int(parts[1]) + 1
        else:
            number = 1
        return f"{name} - {number}"

    def context_data_pass(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "context.wizard",
            "name": _("Context"),
            "view_mode": "form",
            "target": "new",
        }


# Use of inheritance and changing the view of sale order form and added the page named "Anything"
class SaleOrder(models.Model):
    _inherit = "sale.order"

    anything = fields.Char(string="Anything")


# Smart button set in res_partner form view
class ResPartner(models.Model):
    _inherit = "res.partner"

    new_selection = fields.Selection(
        selection=[("yes", "Button Visible"), ("no", "Button Not Visible")],
        default="no",
    )
    nothing = fields.Char(string="Nothing")

    @api.onchange("new_selection")
    def onchange_new_selectioon(self):
        for rec in self:
            if rec.new_selection == "yes":
                print("\n\n\n\n\n\nBasti Ka Hastiiiiii")
            else:
                print("\n\n\n\nTumse Na Ho Payegaaaaa")

    # Method for button
    def action_print(self):
        print("\n\n\n -----------Buttn is working----------\n\n\n")
