
Portugal - Saphety EDI
======================

Allows Odoo to electronically transmit CIUS-PT enabled invoices to the
Saphety EDI platform in order to have them delivered to your customer.


Installation
============

Just install.

Configuration
=============

Enter your Saphety platform username and password on the Saphety EDI zone of
the Portugal section on the Invoicing/Accounting settings.

For testing purposes, you can use these credentials:

- username: sin_api_documentation_user@saphety.com
- password: request_password

Usage
=====

There are no special usage instructions.

As soon as the module is installed, there'll be a submission process on the
Saphety platform for every invoice that produces a CIUS-PT XML attachment.

A cron job will be responsible for following up on the document submission and
integration status. You can see the updated info on the Saphety EDI section of
the Other Info tab on the invoice form.

This information update has 2 distinct stages. As the submission process is
asynchronous, you'll initially receive updates on the submission request
itself. When the it's completed, its state becomes Finished and you'll receive
a submitted document id. After that you'll receive updates on the actual
document's state (delivered to customer, paid, etc...).

Credits
========

Contributors
------------

* `Exo Software <https://exosoftware.pt>`_:

  * João Costa <joao.costa@exo.pt>
  * Pedro Castro Silva <pedrocs@exo.pt>


Maintainer
----------

This module is maintained by Exo Software, Lda.

.. image:: https://exosoftware.pt/logo.png
   :alt: Exo Software
   :target: https://exosoftware.pt
   :width: 100px
