##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author
{
    "name": "Portugal - E-invoicing CIUS-PT",
    "category": "Accounting/Localizations/EDI",
    "summary": "Portuguese e-invoicing (CIUS-PT 2.1.1)",
    "version": "14.0.1.0.0",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "depends": ["ptplus", "account_edi_ubl_cii"],
    "data": [
        "data/cius_pt_211_templates.xml",
        "data/account_edi_data.xml",
    ],
    "installable": True,
    "application": False,
    "license": "OPL-1",
}
