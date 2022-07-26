from odoo import models, fields


class employees(models.Model):
    _inherit = "hr.employee"

    nums = fields.Integer(string="Nº segurado", required="True")
    cp = fields.Char(string="CP")
    pc = fields.Char(string="P/C")
    ndt = fields.Integer(string="Nº DT")
    sl = fields.Integer(string="SL")
    cs = fields.Char(string="CS")
    cf = fields.Integer(string="CF")
    cep = fields.Integer(string="CEP")
