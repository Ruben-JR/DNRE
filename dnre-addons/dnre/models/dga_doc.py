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
    dga = fields.One2many('dga.Lines', string="DGA Lines", readonly="True")

class dgaLines(models.Model):
    _name = 'dga.Lines'
    _description = "DGA Funcionarios"

    dga_id = fields.Many2one('dnre.dga_doc', string="dga", readonly="True")
    