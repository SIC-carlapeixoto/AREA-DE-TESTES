
Portugal - Self-billing
=======================

Install this module to allow self-billing, which is an invoicing process where
a company invoices itself on behalf of a supplier.


Installation
============

Just install.

Configuration
=============

* To allow self-billing invoices for a supplier, check its Self-billing field.
* If you're planning on transmitting the self-billing invoices via webservices to the Tax Authority you should fill the vendor's credentials.
* Create a fiscal document type for that partner's self billing invoices. Don't forget to check the self-billing flag and fill the self-billing partner. You must also create a new sequence for the vendor's self-bills.

Usage
=====

To issue and print self-billing invoices:
* On a vendor bill, activate the Self-billing option. You'll then be able to select the fiscal document type you created on the previous step.
* Validate the invoice.
* Use the Print Self-bill button to obtain the related pdf document. The document will look as if the vendor is the issuer and your company is the customer.

To export the SAF-T file for a self-billing partner:
THIS SECTION IS INCOMPLETE

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
