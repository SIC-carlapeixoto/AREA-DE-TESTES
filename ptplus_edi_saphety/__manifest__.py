##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author
{
    "name": "Portugal - Saphety EDI",
    "category": "Accounting/Localizations/EDI",
    "summary": "Transmit your e-invoices to the Saphety EDI platform",
    "version": "14.0.1.1.0",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "depends": ["ptplus_edi"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/account_move_views.xml",
        "data/ir_cron.xml",
    ],
    "installable": True,
    "application": False,
    "license": "OPL-1",
}
