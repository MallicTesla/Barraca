# -*- coding: utf-8 -*-
import re

import xmltodict
import requests

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    consulta_rut = fields.Boolean()
    xml_result = fields.Text(readonly=True)

    def get_param(self, param=None):
        self = self.sudo()
        # param_obj = self.env['res.company'].with_company(self.env.company).sudo()
        company = self.env.company
        result = getattr(company, param)
        if not result:
            raise ValidationError('No se ha configurado el parámetro ' + param)
        return result

    def to_tree(self, cfe):
        return xmltodict.parse(cfe)

    def find_city(self, name=None):
        name = name.capitalize()
        city_obj = self.env['res.country.city']
        city_id = city_obj.search([('name', '=', name)], limit=1)
        if not city_id:
            city_id = self.env.company.partner_id.city_id
        return city_id

    def find_state(self, name=None):
        name = name.capitalize()
        city_obj = self.env['res.country.state']
        state_id = city_obj.search([('name', '=', name)], limit=1)
        if not state_id:
            state_id = self.env.company.partner_id.state_id
        return state_id

    def load_dgi_data(self, xml_result=None):
        partner = self
        Partner = self.env['res.partner']
        datos_webservice = xmltodict.parse(xml_result)
        datos_persona = datos_webservice.get('WS_PersonaActEmpresarial', {})

        # Extraer datos relevantes con valores por defecto
        denominacion = datos_persona.get('Denominacion', 'Nombre no disponible')
        nombre_fantasia = datos_persona.get('NombreFantasia', 'Nombre de fantasía no disponible')
        tipo_entidad = datos_persona.get('TipoEntidad', 'Tipo de entidad no disponible')
        estado_actividad = datos_persona.get('EstadoActividad', 'Estado de actividad no disponible')
        # Obtener datos de la dirección fiscal
        datos_direccion = datos_persona.get('WS_DomFiscalLocPrincipal', {}).get('WS_PersonaActEmpresarial.WS_DomFiscalLocPrincipalItem', {})
        # Actualizar los campos del partner
        city_id = self.find_city(name=datos_direccion.get('Dpto_Nom'))
        if not city_id:
            state_id = self.find_state(name=datos_direccion.get('Dpto_Nom'))
        calle_nom = datos_direccion.get('Calle_Nom', False)
        if not calle_nom or calle_nom is None:
            calle_nom = 'Calle no disponible'
        valores_a_actualizar = {
            'name': nombre_fantasia if nombre_fantasia else denominacion,
            'social_reason': denominacion,
            'is_company': True,
            'street':calle_nom ,
            'street2': datos_direccion.get('Dom_Pta_Nro', ''),
            'city_id': city_id.id,
            'state_id': city_id.state_id.id if city_id else state_id.id,
            'zip': datos_direccion.get('Dom_Pst_Cod', ''),
            # Añadir más campos según sea necesario
        }

        # Realizar la actualización
        # Manejar contactos (child_ids)
        datos_direccion = datos_persona.get('WS_DomFiscalLocPrincipal', {}).get('WS_PersonaActEmpresarial.WS_DomFiscalLocPrincipalItem', {})
        contactos = datos_direccion.get('Contactos', {}).get('WS_Domicilio.WS_DomicilioItem.Contacto', [])
        if isinstance(contactos, dict):
            contactos = [contactos]
        for contacto in contactos:
            tipo_contacto = contacto.get('TipoCtt_Id')
            valor_contacto = contacto.get('DomCtt_Val')
            if tipo_contacto == '6':  # Suponiendo que '6' es el tipo para teléfonos movil
                valores_a_actualizar['mobile'] = valor_contacto
            elif tipo_contacto == '1':  # Suponiendo que '1' es el tipo para correos electrónicos
                valores_a_actualizar['email'] = valor_contacto
            elif tipo_contacto == '5':  # Suponiendo que '5' es el tipo para teléfonos fijo
                valores_a_actualizar['phone'] = valor_contacto

        partner.update(valores_a_actualizar)
        # self.env.cr.commit()
        if self._origin:
            self._origin.message_post(subject='Datos actualizados desde DGI', body=valores_a_actualizar, message_type='comment')

        return True

    def _consultar_partner_ruc(self):
        api_url = self.get_param('api_server_url')
        url = api_url + f'/?vat={self.vat}'
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise ValidationError('Error al consultar el RUC')
        self.load_dgi_data(response.text)
        self.xml_result = response.content

        return
    @api.onchange('consulta_rut')
    def onchange_consulta_rut(self):
        if self.consulta_rut:
            self._consultar_partner_ruc()