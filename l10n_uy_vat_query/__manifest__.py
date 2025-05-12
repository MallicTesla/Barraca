# -*- coding: utf-8 -*-
{
    'name': "Consulta de RUT en DGI",

    'summary': """
        API para consultar los datos de un RUT en el servicio de DGI

""",

    'description': """
        Documentacion completa para API para consultar los datos de un RUT en el servicio de DGI
        https://documenter.getpostman.com/view/11160626/2sA3drGELi
    """,

    'author': "Primate, Proyectasoft",
    'website': "primate.uy",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'l10n_uy_einvoice_base'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/res_config_settings.xml',
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',

}
