
Portugal - Tax Statements
=========================

This module installs the portuguese tax statements, including

* VAT Periodic Statement
* VAT Yearly Statement
* VAT Recapitulative Statement

VAT Recapitulative Statement
----------------------------

This statement exports a summary of the B2B non-exempt intra-community invoice
lines. It also contains a section for B2B non-exempt intra-community consignment
invoices and returns.

The criteria for selecting B2B intra-community operations on both sections is:
* The destination/origin country must be part of the Europe group (except Portugal).
* The lines have a tax tagged with PT-IVA RG INTRACOM.

In the regular invoices section, the credit note values are subtracted from the
invoice values. If there's only credit notes on a given period, the values would
be negative. To avoid it, negative values are reset to zeros.

You can mark a statement as being a substitution statement but all the substitution
options must be handled on the tax authority website after importing the XML file.


Installation
============




Credits
========

Contributors
------------

- Pedro Castro Silva (`Exo Software <https://exosoftware.pt>`_)


Maintainer
----------

This module is maintained by Exo Software, Lda.

.. image:: https://exosoftware.pt/logo.png
   :alt: Exo Software
   :target: https://exosoftware.pt
   :width: 100px
