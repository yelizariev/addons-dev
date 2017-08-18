# -*- coding: utf-8 -*-
{
    "name": """QR support in POS""",
    "summary": """Technical module to generate or scan QR codes""",
    "category": "Point of Sale",
    # "live_test_URL": "",
    "images": [],
    "version": "1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "point_of_sale",
    ],
    "external_dependencies": {"python": [
        "qrtools",
    ], "bin": []},
    "data": [
        "views/assets.xml",
    ],
    "qweb": [
        "static/src/xml/{QWEBFILE1}.xml",
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
