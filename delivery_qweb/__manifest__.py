{
    "name": "Delivery Report",
    "version": "15.0.0",
    "description": """This module is for qweb report of delivery.""",
    "depends": ["sale", "stock"],
    "data": ["views/stock_move_line_view.xml", "report/report_deliveryslip.xml"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
