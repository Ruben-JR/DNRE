from odoo import models, fields, api


class dgci_doc(models.Model):
    _name = "dnre.dgci_doc"
    _auto = False
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente", required=True)
    dc = fields.Char(string="Designação contribuente", required=True)
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dgci = fields.One2many("dnre.dgci", "dgci_id", string="DGCI lines", readonly="True")

    # @api.depends("nc")
    # def init(self):
    #    self._cr.execute(
    #        """
    #        CREATE OR REPLACE VIEW dnre_dgci_doc AS(
    #            SELECT row_number() over () AS id,
    #            sol.nc, sol.dc, sol.ca, sol.da, sol.mr, sol.tc, sol.r, sol.dga
    #            FROM dnre.dgci_doc sol
    #            LEFT JOIN dnre_dga so ON (so.id = dga_id)
    #        )
    #    """
    #    )


class dgci(models.Model):
    _name = "dnre.dgci"
    _description = "DGCI Funcionarios"

    dgci_id = fields.Many2one("dnre.dgci_doc", string="dgci", readonly="True")
    nums = fields.Integer(string="Nº segurado", required=True)
    ns = fields.Char(string="Nome segurado", required=True)
    cp = fields.Char(string="CP")
    pc = fields.Char(string="P/C")
    ndt = fields.Integer(string="Nº DT")
    sl = fields.Integer(string="SL")
    cs = fields.Char(string="CS")
    cf = fields.Integer(string="CF")
    cep = fields.Integer(string="CEP")
