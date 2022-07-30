from odoo import fields, models, api


class fos(models.Model):
    _name = "dnre.fos_dga"
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente")
    dc = fields.Char(string="Designação contribuente")
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dga_ids = fields.One2many("dnre.dga", "dga_id")

    def get_datas(self):
        department = self.env["hr.department"].search([])
        for d in department:
            if d.name == "DGA":
                self.nc = d.nc
                self.dc = d.dc
                self.ca = d.ca
                self.da = d.da
                self.mr = d.mr
                self.tc = d.tc
                self.r = d.r


class dga(models.Model):
    _name = "dnre.dga"
    _description = "DGA Funcionarios"

    nums = fields.Integer(string="Nº segurado", required=True)
    ns = fields.Char(string="Nome segurado", required=True)
    cp = fields.Char(string="CP")
    pc = fields.Char(string="P/C")
    ndt = fields.Integer(string="Nº DT")
    sl = fields.Integer(string="SL")
    cs = fields.Char(string="CS")
    cf = fields.Integer(string="CF")
    cep = fields.Integer(string="CEP")
    dga_id = fields.Many2one("dnre.fos_dga", readonly="True")

    def get_datas_employees(self):
        employee = self.env["hr.employee"].search([])
        for e in employee:
            self = e
