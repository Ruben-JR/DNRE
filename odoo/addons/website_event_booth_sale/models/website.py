# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def sale_product_domain(self):
        return (
            ["&"]
            + super().sale_product_domain()
            + [("detailed_type", "!=", "event_booth")]
        )
