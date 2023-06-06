# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import calendar


class MedicineInformation(models.Model):
    _name = "medicine.information"
    _rec_name = "medicine_name"

    batch_no = fields.Char(string="Batch No", readonly=True)
    medicine_name = fields.Char(string="Medicine Name")
    reference_number = fields.Char(string="Reference Number")
    manufacturer = fields.Char(string="Manufacturer")
    is_major = fields.Boolean(string="Is major?")
    # expiry_month = fields.Integer(string="Expiry Months")
    dosage_form = fields.Selection(
        selection=[("tablet", "Tablet"), ("capsule", "Capsule"), ("liquid", "Liquid")],
        string="Dosage Form",
    )
    # symptoms_id = fields.Many2one("health.symptoms", string="Symptoms")
    manufacture_date = fields.Date(string="Manufacturing Date")
    # remaining_months = fields.Char(string="Remaining Months", compute="compute_remaining_months")
    expiry_date = fields.Date(string="Expiry Date")

    # default_get method
    @api.model
    def default_get(self, fields):
        res = super(MedicineInformation, self).default_get(fields)
        if "manufacturer" in fields:
            res["manufacturer"] = "SunPharma"
        return res

    # name_get method
    def name_get(self):
        result = []
        for rec in self:
            if rec.expiry_date:
                name = rec.medicine_name + " [" + str(rec.expiry_date) + "]"
                result.append((rec.id, name))
        return result

    # name_search method
    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if name:
            args = [
                "|",
                "|",
                ("medicine_name", operator, name),
                ("reference_number", operator, name),
                ("expiry_date", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    # Write method if expiry date is less than current date:
    def write(self, vals):
        if not vals.get("expiry_date"):
            raise ValidationError("The expiry date is invalid.")
        else:
            current_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
            if current_date > vals.get("expiry_date"):
                raise ValidationError("The expiry date is invalid.")
        return super(MedicineInformation, self).write(vals)

    # Create methos for batch number:
    @api.model
    def create(self, vals):
        if not vals.get("name"):
            seq = self.env["ir.sequence"].next_by_code("medicine.information")
            vals["batch_no"] = (
                seq[0:3]
                + "/"
                + datetime.date.today().strftime("%b").upper()
                + "/"
                + seq[3:]
            )
        return super(MedicineInformation, self).create(vals)

    # To fill the manufacturing date if the medicine name is present:
    @api.onchange("medicine_name")
    def onchange_date(self):
        if self.medicine_name:
            self.manufacture_date = datetime.date.today()
            # self.expiry_month = 12

    # Computer field to count the remaining month from manufacturing date to current date:(if expiry month is given)
    # def compute_remaining_months(self):
    # 	today = datetime.date.today()
    # 	month_difference = 0
    # 	for rec in self:
    # 		if rec.manufacture_date:
    # 			month_difference = (today.year - rec.manufacture_date.year) * 12 + (today.month - rec.manufacture_date.month)
    # 			if rec.expiry_month > month_difference:
    # 				rec.remaining_months = rec.expiry_month - month_difference
    # 			else:
    # 				rec.remaining_months = "Expired"
    # 		else:
    # 			rec.remaining_months = "Invalid"
