# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SIC Medicine Barcodes',
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Parse Medicine GS1 Barcodes',
    'depends': ['barcodes', 'barcodes_gs1_nomenclature', 'stock_barcode'],
    'data': [
        'data/barcodes_gs1_rules.xml',
        'views/stock_move_line_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'sic_med_gs1_barcodes/static/src/js/barcode_parser.js',
            'sic_med_gs1_barcodes/static/src/js/barcode_model.js',
            'sic_med_gs1_barcodes/static/src/js/barcode_picking_model.js',
        ],
    },
    'license': 'LGPL-3',
}
