
Portugal - E-Fatura
===================

Import supplier invoices from an E-Fatura .csv file:

* For every line in the e-fatura file, a new draft vendor bill or refund will
  be created if there isn't one already inserted with the same vendor and
  vendor reference.
* The vendor itself will also be created if necessary.
* If an e-fatura document already exists in the database, a warning will be
  displayed if its values don't match the e-fatura values.
* The relevant invoice data is saved in a custom table containing all the
  imported e-fatura lines so that the user can check at any time if the
  vendor invoices match their e-fatura data.


Installation
============

Just install.

Configuration
=============

This module adds a new section named 'E-Fatura (Import)' on the Invoicing tab
of the supplier form. In there you can fill the E-Fatura Product and E-Fatura
Tax fields. These values will become the default product and tax values for the
invoice lines created from the e-fatura files.

It's also recommended to create default values for these fields. This way the
invoices for all the new suppliers created from the e-fatura file will have an
invoice line with the default product and tax (otherwise the invoices will be
created without lines).

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
