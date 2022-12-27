##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author
{
    "name": "Portugal - E-Fatura",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "category": "Localization",
    "version": "15.0.4.1.0",
    "depends": ["ptplus_accounting"],
    "external_dependencies": {
        "python": ["bs4", "requests_html"],
    },
    "data": [
        "security/ir.model.access.csv",
        "security/efatura_security.xml",
        "views/account_efatura.xml",
        "views/res_partner_views.xml",
        "views/account_move_views.xml",
        "views/res_config_views.xml",
        "wizards/dataport_import_efatura.xml",
        "wizards/account_move_efatura.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
