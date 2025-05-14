import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class OrdenVenta(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """Extiende Confirmar para ejecutar TODOS los cron jobs de tipo 'code'
           justo después de cerrar la transacción de confirmación."""
        # 1) Confirmar la orden
        resultado = super(OrdenVenta, self).action_confirm()

        # 2) Forzar commit de la confirmación (cierra la tx antes de lanzar los crons)
        try:
            self.env.cr.commit()
        except Exception:
            _logger.exception("00000000000 Error al hacer commit tras confirmación")

        # 3) Disparar todos los ir.cron de tipo 'code' (incluye tu Automatic Workflow Job)
        trabajos_cron = self.env['ir.cron'].search([('state', '=', 'code')])
        for trabajo in trabajos_cron:
            try:
                trabajo.method_direct_trigger()
            except Exception:
                _logger.exception("1111111111111111 Error al ejecutar cron %s", trabajo.name)

        return resultado




