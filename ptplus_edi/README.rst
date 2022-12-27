
Portugal - E-invoicing (CIUS-PT 2.1.1)
======================================

Adds CIUS-PT enabled invoicing to Odoo according to the CIUS-PT 2.1.1 dated
26-Feb-2021 norm published by the (`eSPap <https://www.espap.gov.pt/spfin/normas/Paginas/normas.aspx>`_).

An XML file will be created and attached to every sales invoice. Additionally,
it will be included on the Send by Mail feature.

Note: importing CIUS-PT invoices is still WIP.

Installation
============

Just install

Configuration
=============

After module installation you'll see a new option on every sales journal that
belongs to a Portuguese company. It's called CIUS-PT 2.1.1 (PT) and it's
available on the Electronic Data Interchange section. When active, the CIUS-PT
rules will be enforced and an XML file will be added to every invoice or credit
note issued on the journal.

You can have multiple sales journal, some of them with CIUS-PT activation and
others without it.

Usage
=====

No instruction needed.

Credits
========

Contributors
------------

* `Exo Software <https://exosoftware.pt>`_:

  * Pedro Castro Silva <pedrocs@exo.pt>


Maintainer
----------

This module is maintained by Exo Software, Lda.

.. image:: https://exosoftware.pt/logo.png
   :alt: Exo Software
   :target: https://exosoftware.pt
   :width: 100px
