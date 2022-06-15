# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dgci_doc(models.Model):
    _name = 'dnre.dgci_doc'
    _auto = False
    _description = "DNRE - Recursos Humanos"

    nc = fields.Integer(string="Nº contribuente", required=True)
    dc = fields.Char(string="Designação contribuente", required=True)
    ca = fields.Integer(string="CA")
    da = fields.Char(string="DA")
    mr = fields.Date(string="MR")
    tc = fields.Integer(string="TC")
    r = fields.Char(string="Regime")
    dgci = fields.One2many('dnre.dgci.Lines', string="DGCI lines", readonly="True")

class dgciLines(models.Model):
    _name = 'dgci.Lines'
    _description = "DGCI Funcionarios"

    dgci_id = fields.Many2one('dnre.dgci', string="dgci", readonly="True")
