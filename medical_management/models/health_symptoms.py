# -*- coding: utf-8 -*-

from odoo import models, fields


class HealthSymptoms(models.Model):
    _name = "health.symptoms"

    name = fields.Char(string="Symptoms")

    def action_medicine_info(self):
        model_rec = self.env["medicine.information"].search_count([])
        print("\n\n\n Model Record Count:", model_rec)
