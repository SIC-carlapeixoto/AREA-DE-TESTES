##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author

{
    "name": "Portugal - Full Accounting",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "category": "Localization",
    "version": "15.0.4.0.0",
    "depends": ["account", "ptplus", "ptplus_account_credit_note"],
    "data": [
        "data/account_tax_data.xml",
        "data/account_taxonomy_data.xml",
        "data/account_asset_legal_rate.xml",
        "security/ir.model.access.csv",
        "security/accounting_security.xml",
        "views/account_balance_transfer.xml",
        "views/account_taxonomy.xml",
        "views/account_account_views.xml",
        "views/account_journal_views.xml",
        "views/account_tax_views.xml",
        "views/account_move_views.xml",
        "views/report_account_move.xml",
        "views/account_asset_legal_rate_views.xml",
        "report/account_move_report.xml",
        "wizards/account_taxonomy_setup_wizard.xml",
        "wizards/account_tax_tag_setup_wizard.xml",
        # "wizards/account_invoice_refund_views.xml",
        "wizards/account_move_reversal_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "demo": [],
    "installable": True,
}
