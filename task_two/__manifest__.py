{
    "name": "Product Information",
    "version": "15.0.0",
    "description": """This module to add other information of product in sale, stock and invoice.""",
    "depends": ["sale_management", "stock", "account"],
    "data": [
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
