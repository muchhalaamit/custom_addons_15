from odoo import models, fields
import datetime


class MedicineSymptomsInformation(models.Model):
    _name = "medicine.symptoms.information"
    # _rec_name = "medicine_id"
    current_date = datetime.datetime.now().date().strftime("%Y-%m-%d")

    medicine_id = fields.Many2one(
        "medicine.information",
        domain=[("expiry_date", ">", current_date)],
        string="Medicine",
    )
    symptoms_ids = fields.Many2many("health.symptoms", string="Symptoms")
