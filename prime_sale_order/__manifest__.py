{
    "name": "Prime Sale",
    "version": "15.0.1.0.0",
    "description": """This module to add prime sale order.""",
    "depends": ["sale_management", "stock"],
    "data": [
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
