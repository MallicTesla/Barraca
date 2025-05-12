from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger("SERVICIOS DE FACTURACION ELECTRONICA")
API_URL = 'https://consultarut.proyectasoft.com/api/vat_query'


def post_init_hook(env):
    print('START OPERATION')
    _logger.info('STARTS--> LOAD API SERVER URL FOR COMPANIES')
    companies = env['res.company'].search([])
    for company in companies:
        company.api_server_url = API_URL
