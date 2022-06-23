# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "eCommerce",
    "category": "Website/Website",
    "sequence": 50,
    "summary": "Sell your products online",
    "website": "https://www.odoo.com/app/ecommerce",
    "version": "1.1",
    "description": "",
    "depends": [
        "website",
        "sale",
        "website_payment",
        "website_mail",
        "portal_rating",
        "digest",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/website_sale.xml",
        "data/data.xml",
        "data/mail_template_data.xml",
        "data/product_snippet_template_data.xml",
        "data/digest_data.xml",
        "views/product_attribute_views.xml",
        "views/product_views.xml",
        "views/account_views.xml",
        "views/onboarding_views.xml",
        "views/sale_report_views.xml",
        "views/sale_order_views.xml",
        "views/crm_team_views.xml",
        "views/templates.xml",
        "views/snippets/snippets.xml",
        "views/snippets/s_dynamic_snippet_products.xml",
        "views/res_config_settings_views.xml",
        "views/digest_views.xml",
        "views/website_sale_visitor_views.xml",
        "views/base_unit_view.xml",
    ],
    "demo": [
        "data/demo.xml",
    ],
    "installable": True,
    "application": True,
    "post_init_hook": "_post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "assets": {
        "web.assets_frontend": [
            "website_sale/static/src/scss/website_sale.scss",
            "website_sale/static/src/scss/website_mail.scss",
            "website_sale/static/src/scss/website_sale_frontend.scss",
            "website/static/lib/multirange/multirange_custom.scss",
            "sale/static/src/scss/sale_portal.scss",
            "sale/static/src/scss/product_configurator.scss",
            "sale/static/src/js/variant_mixin.js",
            "website_sale/static/src/js/variant_mixin.js",
            "website_sale/static/src/js/website_sale.js",
            "website_sale/static/src/js/website_sale_utils.js",
            "website_sale/static/src/js/website_sale_payment.js",
            "website_sale/static/src/js/website_sale_validate.js",
            "website_sale/static/src/js/website_sale_recently_viewed.js",
            "website_sale/static/src/js/website_sale_tracking.js",
            "website/static/lib/multirange/multirange_custom.js",
            "website_sale/static/src/js/website_sale_category_link.js",
        ],
        "web._assets_primary_variables": [
            "website_sale/static/src/scss/primary_variables.scss",
        ],
        "web.assets_backend": [
            "website_sale/static/src/js/website_sale_video_field_preview.js",
            "website_sale/static/src/js/website_sale_backend.js",
            "website_sale/static/src/scss/website_sale_dashboard.scss",
            "website_sale/static/src/scss/website_sale_backend.scss",
            "website_sale/static/src/js/tours/website_sale_shop_backend.js",
        ],
        "website.assets_wysiwyg": [
            "website_sale/static/src/scss/website_sale.editor.scss",
            "website_sale/static/src/snippets/s_dynamic_snippet_products/options.js",
        ],
        "website.assets_editor": [
            "website_sale/static/src/js/website_sale.editor.js",
            "website_sale/static/src/js/website_sale_form_editor.js",
            "website_sale/static/src/js/tours/website_sale_shop_frontend.js",
        ],
        "web.assets_common": [
            "website_sale/static/src/js/tours/tour_utils.js",
            "website_sale/static/src/js/tours/website_sale_shop.js",
        ],
        "web.assets_tests": [
            "website_sale/static/tests/**/*",
        ],
        "web.assets_qweb": [
            "website_sale/static/src/xml/*.xml",
        ],
    },
    "license": "LGPL-3",
}
