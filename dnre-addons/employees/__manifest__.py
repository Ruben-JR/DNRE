{
    "name": "employees",
    "summary": """
        Direção Nacional de Receitas do Estado""",
    "description": """
        Funcionários DNRE
    """,
    "author": "Ruben de Pina",
    "website": "https://mf.gov.cv/web/dnre",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Dnre/employees",
    "sequence": -99,
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["hr"],
    # always loaded
    "data": [
        #'security/ir.model.access.csv',
        "views/views.xml",
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
