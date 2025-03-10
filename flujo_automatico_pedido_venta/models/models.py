# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class flujo_automatico_pedido_venta(models.Model):
#     _name = 'flujo_automatico_pedido_venta.flujo_automatico_pedido_venta'
#     _description = 'flujo_automatico_pedido_venta.flujo_automatico_pedido_venta'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

