from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_prime_customer = fields.Boolean(string="Is Prime Customer?")
    prime_discount = fields.Float(string="Discount")

    @api.constrains("prime_discount")
    def _check_discount(self):
        for rec in self:
            if rec.prime_discount < 0 or rec.prime_discount > 100:
                raise ValidationError("The discount entered is invalid.")
