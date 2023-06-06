from odoo import fields, models


class SaleOrderLine(models.Model):
    """Inheriting sale_order-line to show the field named "ref" """

    _inherit = "sale.order.line"

    other_information = fields.Char(string="Other Information")

    def _prepare_invoice_line(self, **optional_values):
        rec = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        rec.update({"other_information": self.other_information})
        return rec
