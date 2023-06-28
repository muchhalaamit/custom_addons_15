from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class ContactForm(http.Controller):
    @http.route(["/contact"], type="http", auth="public", website=True, sitemap=False)
    def contact_view(self, **post):
        res_partner_records = request.env["res.partner"].sudo().search([])
        print("::::::::::;;res_partner_records", res_partner_records)
        records = {
            "name": res_partner_records,
        }
        return request.render("bulk_product.res_partner_data_view", records)


class Test(WebsiteSale):
    def sitemap_shop(env, rule, qs):
        print(":::::::::::::::::sitemap_shop")
        return super(Test).sitemap_shop(env, rule, qs)

    @http.route(
        [
            """/shop""",
            """/shop/page/<int:page>""",
            """/shop/category/<model("product.public.category"):category>""",
            """/shop/category/<model("product.public.category"):category>/page/<int:page>""",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_shop)
    def shop(self, page=0, category=None, search="", min_price=0.0, max_price=0.0, ppg=False, **post):
        print(":::::::::::::::::::inherit before")
        res = super(Test, self).shop(
                page=page,
                category=category,
                search=search,
                min_price=min_price,
                max_price=max_price,
                ppg=ppg,
                **post)
        print(":::::::::::::::::::inherit after")
        return res
