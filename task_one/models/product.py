from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        if (
            "search_default_my_quotation" or "default_description_sale" in self._context
        ) and "active_model" not in self._context:
            return [(product.id, product.name) for product in self]
        else:
            return super(ProductProduct, self).name_get()
