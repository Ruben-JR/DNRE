from odoo import models, fields, api


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

    @api.model
    def __init__(self):
        self.env.cr.execute(
            """
            SELECT fos.nc, fos.dc, fos.ca, fos.da, fos.mr, fos.tc, fos.r
            FROM dnre.fos AS fos,
            INNER JOIN dnre.dga AS dga
            ON fos.dga_ids = dga.dga_id
            INNER JOIN dnre.dgci AS dgci
            ON fos.dgci_ids = dgci.dgci_ids
        """
        )
        self.env.cr.fetchall()


# fos.nc as nc, fos.dc as dc, fos.ca as ca, fos.da as da, fos.mr as mr, fos.tc as tc, fos.r as r


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
