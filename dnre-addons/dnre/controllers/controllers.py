from odoo import http


class Dnre(http.Controller):
    @http.route("/dnre/dnre", auth="public")
    def index(self, **kw):
        return "Hello, world"

    @http.route("/dnre/dnre/objects", auth="public")
    def list(self, **kw):
        return http.request.render(
            "dnre.listing",
            {
                "root": "/dnre/dnre",
                "objects": http.request.env["dnre.dnre"].search([]),
            },
        )

    @http.route('/dnre/dnre/objects/<model("dnre.dnre"):obj>', auth="public")
    def object(self, obj, **kw):
        return http.request.render("dnre.object", {"object": obj})
