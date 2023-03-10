
Portugal - Full Accounting
==========================

The base module for handling Portuguese full accounting in Odoo. Mods include:

- SNC taxonomy support
- a template based account balance transfer tool. A template for P/L Calculation
  is included for every company.
- new journal types: p/l calculation, fiscal year regularization and adjustment
- a report for printing journal entries
- vat adjustment norms to be applied on credit and debit notes

Installation
============

The installation process creates a balance transfer template for P/L calculation
on every company that has a CoA installed. The same template will be automatically
installed on new companies upon CoA creation. This template has 3 transfers:

* Income and Expense (6 and 7) to 811 - Results before taxes
* Tax estimate and cut off taxes from 812 into 818 - Net result
* 811 - Results before taxes into 818 - Net result

Configuration
=============

If for any reason, the P/L calculation is not installed on a company you can try
to manually create it using the option available on the Action button on the
company form.

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
