from odoo import models, fields, api, tools


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

    @api.depends("nc")
    def __init__(self, pool, cr):
        tools.drop_view_if_exists(self.nc, self._table)
        self.nc(
            """
            SELECT dnre.fos.nc, dnre.fos.dc, dnre.fos.ca, dnre.fos.da, dnre.fos.mr, dnre.fos.tc, dnre.fos.r, dnre.fos.dga_ids, dnre.fos.dgci_ids
                   dnre.dga.nums, dnre.dga.ns, dnre.dga.cp, dnre.dga.pc, dnre.dga.ndt, dnre.dga.sl, dnre.dga.cs, dnre.dga.cf, dnre.dga.cep,
                   dnre.dgci.nums, dnre.dgci.ns, dnre.dgci.cp, dnre.dgci.pc, dnre.dgci.ndt, dnre.dgci.sl, dnre.dgci.cs, dnre.dgci.cf, dnre.dgci.cep,
            FROM dnre.fos,
            INNER JOIN dnre.dga
            ON dnre.fos.dga_ids = dnre.dga.dga_id
            INNER JOIN dnre.dgci
            ON dnre.fos.dgci_ids = dnre.dgci.dgci_id
        """
        )
        # self.env.cr.fetchall()


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
