====================
Portugal - Invoicing
====================

This module adds the fields and views that are needed for the base portuguese localization.
The ultimate goal is to allow an organization to change Odoo provider with minimum
impact. Added features/fields include (with no particular order):

* Support for debit notes and simplified invoices (invoice-like document types)
* Support for delivery notes and similar documents
* Pre-defined legally accepted reasons for issuing credit notes, as required for fields 40/41 of the VAT statement (Portaria nº 255/2013).
* Fields required for document signing certification: Hash, HashControl, SystemEntryDate, SourceID, etc...
* Tax related fields:
    Genre (VAT, Stamp duty, etc...)
    VAT type (normal, intermediate, reduced, exempt)
    Country region (Continental Portugal, Azores, Madeira, EC, Outside EC)
    VAT exemption reason (legally accepted reason for issuing VAT exempt invoice lines)
* Account Taxonomies (Portaria nº 302/2016)

Change the standard graphical layout and print behaviour of documents that are
controlled by the Portuguese Tax Authorities, namely:


- Add simplified invoices and debit notes
- Credit note accounting is mapped to user-defined refund accounts
- Credit and Debit notes include VAT Adjustment Norms and related info

Installation
============

Just do it.

Credits
========

Contributors
~~~~~~~~~~~~

- Pedro Castro Silva (`Exo Software <https://exosoftware.pt>`_)


Maintainer
----------

This module is maintained by Exo Software, Lda.

.. image:: https://exosoftware.pt/logo.png
   :alt: Exo Software
   :target: https://exosoftware.pt
   :width: 100px
