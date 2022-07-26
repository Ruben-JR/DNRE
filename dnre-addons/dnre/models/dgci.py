from odoo import fields, models


class fos(models.Model):
    _name = "dnre.fos_dgci"
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente", required=True)
    dc = fields.Char(string="Designação contribuente", required=True)
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dgci_ids = fields.One2many("dnre.dgci", "dgci_id")


class dgci(models.Model):
    _name = "dnre.dgci"
    _description = "DGCI Funcionarios"

    nums = fields.Integer(string="Nº segurado", required=True)
    ns = fields.Char(string="Nome segurado", required=True)
    cp = fields.Char(string="CP")
    pc = fields.Char(string="P/C")
    ndt = fields.Integer(string="Nº DT")
    sl = fields.Integer(string="SL")
    cs = fields.Char(string="CS")
    cf = fields.Integer(string="CF")
    cep = fields.Integer(string="CEP")
    dgci_id = fields.Many2one("dnre.fos", readonly="True")
