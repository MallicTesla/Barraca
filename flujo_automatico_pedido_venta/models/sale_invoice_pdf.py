from odoo import models, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_download_invoice_pdf(self):
        self.ensure_one()
        invoice = self.invoice_ids.filtered(lambda inv: inv.state == 'posted')
        if not invoice:
            raise UserError(_("No hay una factura publicada asociada a esta orden de venta."))
        return self.env.ref('account.account_invoices').report_action(invoice)

