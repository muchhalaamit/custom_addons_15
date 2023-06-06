# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class EmployeeSalary(models.Model):
    _name = "employee.salary"
    _description = "Employee Salary"
    _rec_name = "salary_amount"

    salary_amount = fields.Integer(string="Salary(Monthly)")
    employee_id = fields.Many2one("employee.details", string="Employee")
