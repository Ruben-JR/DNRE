from odoo import models, fields


class fos(models.Model):
    _name = "dnre.fos"
    _auto = False
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente", required=True)
    dc = fields.Char(string="Designação contribuente", required=True)
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dga_ids = fields.One2many("dnre.dga", "dga_id", string="DGA Lines", readonly="True")
    dgci_ids = fields.One2many(
        "dnre.dgci", "dgci_id", string="DGCI lines", readonly="True"
    )

    def init(self):
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW dnre_fos AS (
                SELECT row_number() OVER() as id,
                so.nums as nums, so.ns as ns, so.cp as cp, so.pc as pc, so.ndt as ndt, so.sl as sl, so.cs as cs, so.cf as cf, so.cep as cep, so.dga.id as dga_ids, so.dgci.id = dgci_ids
                FROM dnre_fos
                JOIN dnre_dga ON so.dga_ids = dga.id
                JOIN dnre_dgci ON so dgci_ids = dgci.id
            )
        """
        )


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
    dga_id = fields.Many2one("dnre.fos", string="dga", readonly="True")


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
    dgci_id = fields.Many2one("dnre.fos", string="dgci", readonly="True")
