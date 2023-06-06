{
    "name": "Branding Object",
    "license": "LGPL-3",
    "category": "Product",
    "version": "15.0.0.0",
    "summary": "This module will allow user to create a branding product.",
    "description": "An app to add branding to product",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/product_views.xml",
        "views/sale_views.xml",
        "report/report_deliveryslip.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
