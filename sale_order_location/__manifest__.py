{
    "name": "Sale Order Location",
    "version": "15.0.1.0.0",
    "description": """This module will allow to add location in sale order.""",
    "depends": ["sale_management", "stock"],
    "data": [
        "security/sale_order_location_security.xml",
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "report/sale_report_templates.xml",
        ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
