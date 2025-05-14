from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('type_id')
    def _onchange_type_id_set_workflow(self):
        """Al cambiar el tipo, asigna el primer flujo automático disponible."""
        for order in self:
            if order.type_id and order.type_id.flujo_automatico_ids:
                order.workflow_process_id = order.type_id.flujo_automatico_ids[0].id
            else:
                order.workflow_process_id = False

    def copy(self, default=None):
        """Al duplicar la cotización, conserva (o vuelve a calcular) el flujo automático."""
        default = dict(default or {})
        # Si al duplicar no vienen explícitamente workflow_process_id
        for order in self:
            if not default.get('workflow_process_id') and order.type_id and order.type_id.flujo_automatico_ids:
                default['workflow_process_id'] = order.type_id.flujo_automatico_ids[0].id
        return super(SaleOrder, self).copy(default)

