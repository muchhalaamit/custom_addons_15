# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class EmployeeDetails(models.Model):
    _name = "employee.details"
    _description = "Employee Details"
    _rec_name = "employee_name"

    employee_name = fields.Char(string="Name")
    employee_age = fields.Integer(string="Age")
    employee_address = fields.Text(string="Address")
    employee_contact = fields.Char(string="Contact No")
    employee_email = fields.Char(string="Email Id")
    employee_position_id = fields.Many2one("employee.position", string="Designation")
    employee_department_id = fields.Many2one("company.department", string="Department")
    # project_id = fields.Many2one("project.details", string="Assigned Project")
