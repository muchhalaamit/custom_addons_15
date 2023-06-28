{
    "name": "Object Branding",
    "version": "15.0.0",
    "description": """This module will allow user to create branding product.""",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/branding_object_view.xml",
        "views/product_template_view.xml",
        "views/sale_order.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
