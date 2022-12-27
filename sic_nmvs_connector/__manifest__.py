# -*- coding: utf-8 -*-
{
    'name': "SIC NMVS Connector",

    'summary': """
        SIC Connector to NMVS""",

    'description': """
        SIC Connector to NMVS
    """,

    'author': "SmartImproveConsulting",
    'website': "https://www.smartimprove.pt",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','sic_med_gs1_barcodes','stock_lock_lot','purchase']
    ,'external_dependencies': {
       'python': ['xmltodict'],
    },

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/nmvs_operation_views.xml',
        'views/product_category_views.xml',
        'views/stock_production_lot_views.xml',
        'views/stock_picking_views.xml',
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'wizard/nmvs_manual_operation_views.xml',
        'wizard/nmvs_mixed_bulk_operation_views.xml',
        'wizard/get_picking_serials_views.xml',
        'wizard/import_product_notification_list_views.xml',
        'report/paperformat.xml',
        'report/report_layouts.xml',
        'report/reports.xml',
        'report/anexo_7.xml',
        'report/pedido_aue.xml',
        'views/nmvs_sequence.xml',
        'views/menu.xml',
    ],    
    'assets': {
        'web.assets_backend': [
            'sic_nmvs_connector/static/src/js/barcode_model.js',
            'sic_nmvs_connector/static/src/js/barcode_picking_model.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
