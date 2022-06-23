# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockRulesReport(models.TransientModel):
    _inherit = "stock.rules.report"

    so_route_ids = fields.Many2many(
        "stock.location.route",
        string="Apply specific routes",
        domain="[('sale_selectable', '=', True)]",
        help="Choose to apply SO lines specific routes.",
    )

    def _prepare_report_data(self):
        data = super()._prepare_report_data()
        data["so_route_ids"] = self.so_route_ids.ids
        return data
