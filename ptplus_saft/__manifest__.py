##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author

{
    "name": "Portugal - SAF-T PT Statement",
    "version": "15.0.4.0.0",
    "license": "OPL-1",
    "depends": ["ptplus"],
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "category": "Localization",
    "data": [
        "security/ir.model.access.csv",
        "wizards/dataport_export_saft.xml",
    ],
    "external_dependencies": {
        "python": [
            "unicodecsv",
        ],
    },
    "installable": True,
    "auto_install": True,
    "application": False,
}
