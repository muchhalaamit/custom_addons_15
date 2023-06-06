from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        sale_attachments = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "sale.order"),
                ("res_id", "=", self._context.get("active_id")),
            ]
        )
        for attachment in sale_attachments:
            attachment.copy({"res_model": "account.move", "res_id": res.id})
        return res
