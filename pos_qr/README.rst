===================
 QR support in POS
===================

Technical module to generate or scan QR codes.

QR generating
-------------

* qr is generated on client side via https://larsjung.de/jquery-qrcode/


QR scanning
-----------

* qr is decoded on server side via `qrtools <https://github.com/primetang/qrtools>`_
* to capture image we use html5 input::

   <input type="file" accept="image/*" id="capture" capture="camera"> 


Credits
=======

Contributors
------------
* Ivan Yelizariev <yelizariev@it-projects.info>

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/pos-addons/10.0

HTML Description: https://apps.odoo.com/apps/modules/10.0/pos_qr

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 084967754870735ab75f9266e6ae9b8189385ab2
