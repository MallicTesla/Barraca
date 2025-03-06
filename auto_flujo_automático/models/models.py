# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class auto_flujo_automático(models.Model):
#     _name = 'auto_flujo_automático.auto_flujo_automático'
#     _description = 'auto_flujo_automático.auto_flujo_automático'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

