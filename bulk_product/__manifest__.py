{
    "name": "Bulk Product",
    "version": "15.0.0",
    "description": """This module of Bulk product""",
    "depends": ["sale", "product", "website", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "data/split_delivery_action.xml",
        "views/bulk_product_view.xml",
        "views/sale_order_inherit.xml",
        "report/sale_order_report_view.xml",
        "report/stock_delivery_slip_report.xml",
        "views/product_template_inherit_view.xml",
        "views/website_sale_template_inherit.xml",
        "views/menu_inherit_view.xml",
        "views/main_view.xml",
        "wizard/split_delivery_wizard_view.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "bulk_product/static/scss/main_view.css",
        ]
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
