=============================
 Website Switcher in Backend
=============================

Installation
============

* Add this module to server-wide modules, for example::

      ./odoo-bin --load=web,web_website
* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way
* As this is a technical module, consider to install other modules that use this one, for example `ir_config_parameter_multi_company <https://apps.odoo.com/apps/modules/10.0/ir_config_parameter_multi_company/>`_

Usage
=====

After installation you will see Website Switcher in top right-hand corner.

Besides, there is a new menu ``[[ Settings ]] >> Technical >> Parameters >> Website Properties`` (available in `Activate Developer <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__)

Uninstallation
==============

Don't forget to remove ``web_website`` from server-wide modules
