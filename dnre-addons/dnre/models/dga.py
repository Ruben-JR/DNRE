# -*- coding: utf-8 -*-

from odoo import models, fields


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
    