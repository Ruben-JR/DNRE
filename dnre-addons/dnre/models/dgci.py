from odoo import models, fields, api


class dgci(models.Model):
   _name = 'dnre.dgci'
   _auto = False
   _description = "DNRE - Recursos Humanos"

   nums = fields.Integer(string="Nº segurado", required=True)
   ns = fields.Char(string="Nome segurado", required=True)
   cp = fields.Char(string="CP")
   pc = fields.Char(string="P/C")
   ndt = fields.Integer(string="Nº DT")
   sl = fields.Integer(string="SL")
   cs = fields.Char(string="CS")
   cf = fields.Integer(string="CF")
   cep = fields.Integer(string="CEP")
   