# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.osv import expression


class SmsTemplate(models.Model):
    _inherit = "sms.template"

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """Context-based hack to filter reference field in a m2o search box to emulate a domain the ORM currently does not support.

        As we can not specify a domain on a reference field, we added a context
        key `filter_template_on_event` on the template reference field. If this
        key is set, we add our domain in the `args` in the `_name_search`
        method to filtrate the SMS templates.
        """
        if self.env.context.get("filter_template_on_event"):
            args = expression.AND([[("model", "=", "event.registration")], args])
        return super()._name_search(name, args, operator, limit, name_get_uid)
