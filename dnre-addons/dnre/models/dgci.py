from odoo import fields, models


class fos(models.Model):
    _name = "dnre.fos_dgci"
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente")
    dc = fields.Char(string="Designação contribuente")
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dgci_ids = fields.One2many("dnre.dgci", "dgci_id")

    def get_datas_dgci(self):
        department = self.env["hr.department"].search([])
        for l in department:
            if l.name == "DGCI":
                self.nc = l.nc
                self.dc = l.dc
                self.ca = l.ca
                self.da = l.da
                self.mr = l.mr
                self.tc = l.tc
                self.r = l.r


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
    dgci_id = fields.Many2one("dnre.fos_dgci", readonly="True")

    def get_datas_dga(self):
        employee = self.env["hr.employee"].search([])
        for l in employee:
            self.nums = l.nums
            self.ns = l.ns
            self.cp = l.cp
            self.pc = l.pc
            self.ndt = l.ndt
            self.sl = l.sl
            self.cs = l.cs
            self.cf = l.cf
            self.cep = l.cep
