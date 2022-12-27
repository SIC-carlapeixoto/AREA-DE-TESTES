##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author

{
    "name": "Portugal - Credit Notes",
    "version": "15.0.4.0.0",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "category": "Localization",
    "depends": ["ptplus", "account_invoice_refund_link"],
    "data": [
        "views/account_move_views.xml",
        "wizards/account_move_reversal_views.xml",
    ],
    "demo": [],
    "auto_install": True,
    "installable": True,
}
