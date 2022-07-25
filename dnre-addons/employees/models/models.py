from odoo import models, fields


class employees(models.Model):
    _name = "employees.employees"
    _description = "employees.employees"
    _inherit = "hr.employee.base"

    nc = fields.Integer(string="Nº contribuente", required=True)
    dc = fields.Char(string="Designação contribuente", required=True)
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
