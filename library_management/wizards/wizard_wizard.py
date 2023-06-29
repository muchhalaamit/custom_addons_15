# -*- coding: utf-8 -*-

from odoo import fields, models, api


class WizardWizard(models.TransientModel):
    _name = "wizard.wizard"
    _description = "Wizard for wizard"

    name =  fields.Char(string="Name")
    age = fields.Integer(string="Age")

    # This is a python function for a wizard button named "Confirm"
    def action_confirm(self):
        print(self)
        print(self._context)
        print("\n\n\nAction Confirm button is pressed")
        print(f"Name: {self.name},\nAge: {self.age}")
