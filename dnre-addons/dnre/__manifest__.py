{
    "name": "DNRE",
    "summary": """
        Direção Nacional de Receitas do Estado""",
    "description": """
        Recursos Humanos
    """,
    "author": "Ruben de Pina",
    "website": "https://mf.gov.cv/web/dnre",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "DNRE - RH",
    "sequence": -100,
    "version": "1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/fos.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
