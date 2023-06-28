# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class CompanyDepartment(models.Model):
    _name = "company.department"
    _description = "Company Department"
    _rec_name = "department_name"

    department_name = fields.Char(string="Department")
    employee_ids = fields.One2many("employee.details", "employee_department_id", string="Employees")
