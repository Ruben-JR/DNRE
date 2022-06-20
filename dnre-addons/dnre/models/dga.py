# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class dga_doc(models.Model):
    _name = 'dnre.dga_doc'
    _auto = False
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente", required=True)
    dc = fields.Char(string="Designação contribuente", required=True)
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dga = fields.One2many('dnre.dga', string="DGA Lines", readonly="True")

    @api.depends('nc')
    def init(self):
            self._cr.execute("""
            CREATE OR REPLACE VIEW dnre_dga_doc AS(
                SELECT row_number() over () AS id,
                sol.nc, sol.dc, sol.ca, sol.da, sol.mr, sol.tc, sol.r, sol.dga
                FROM dnre_dga sol
                LEFT JOIN dnre_dga so ON (so.id = dga_id)
            )     
        """)

class dga(models.Model):
    _name = 'dnre.dga'
    _description = "DGA Funcionarios"

    dga_id = fields.Many2one(string="dga", readonly="True")
    nums = fields.Integer(string="Nº segurado", required=True)
    ns = fields.Char(string="Nome segurado", required=True)
    cp = fields.Char(string="CP")
    pc = fields.Char(string="P/C")
    ndt = fields.Integer(string="Nº DT")
    sl = fields.Integer(string="SL")
    cs = fields.Char(string="CS")
    cf = fields.Integer(string="CF")
    cep = fields.Integer(string="CEP")

    @api.depends('nums')
    def init(self):
            self._cr.execute("""
            CREATE OR REPLACE VIEW dnre_dga AS(
                SELECT row_number() over () AS id,
                sol.dga_id, sol.nums, sol.ns, sol.cp, sol.pc, sol.ndt, sol.sl, sol.cs, sol.cf, sol.cep
                FROM dnre_dga sol
                LEFT JOIN dnre_dga_doc so ON (so.id = id)
            )     
        """)
    