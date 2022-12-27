##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author
{
    "name": "Portugal - Tax Statements",
    "version": "15.0.4.0.0",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "category": "Localization",
    "depends": [
        "ptplus_accounting",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/tax_statement_data.xml",
        "data/account.tax.statement.line.csv",
        "views/account_tax_statement_template.xml",
        "views/account_tax_statement.xml",
        "views/dataport_log.xml",
        "wizards/wizard_tax_statement.xml",
        "wizards/wizard_recap_statement.xml",
    ],
    "demo": [],
    "auto_install": False,
    "installable": True,
}
