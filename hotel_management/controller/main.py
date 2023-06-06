from odoo import fields, http
from odoo.http import request
import base64


class ResData(http.Controller):
    @http.route(["/form"], type="http", auth="public", website=True, sitemap=False)
    def res_data(self, **post):
        country_rec = request.env["res.country"].sudo().search([])
        record = {"country_name": country_rec}
        return request.render("hotel_management.form_template", record)

    @http.route(
        ["/form/submit"], type="http", auth="public", website=True, sitemap=False
    )
    def submit_data(self, **post):
        # with open(post.get("image"), "rb") as f:
        # 	png_encoded = base64.b64encode(f.read())
        # encoded_b2 = "".join([format(n, '08b') for n in png_encoded])
        # print(encoded_b2)
        # print("\n\n", converted_string)
        vals = {
            "name": post.get("name"),
            "street": post.get("street"),
            "street2": post.get("street2"),
            "phone": post.get("phone"),
            "email": post.get("email"),
            "country_id": int(post.get("country")),
        }
        request.env["res.partner"].create(vals)
        return request.render("hotel_management.thank_you_template")
