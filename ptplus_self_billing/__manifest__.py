##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author
{
    "name": "Payment Acquirer Portugal",
    "category": "Accounting/Payment Acquirers",
    "summary": "A base module for portuguese payment methods",
    "version": "15.0.2.0.0",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "depends": ["payment", "l10n_pt"],
    "data": [
        "security/ir.model.access.csv",
        "data/payment_icon_data.xml",
        "data/ir_cron.xml",
        "views/report_templates.xml",
        "views/report_invoice.xml",
        "views/report_sale_order.xml",
        "views/payment_views.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "views/payment_templates.xml",
        "wizard/account_generate_multibanco_views.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "/payment_portugal/static/src/scss/reports.scss",
        ],
    },
    "installable": True,
    "application": False,
    "license": "OPL-1",
}
