# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class EmployeePosition(models.Model):
    _name = "employee.position"
    _description = "Employee Position"

    name = fields.Char(string="Position")
