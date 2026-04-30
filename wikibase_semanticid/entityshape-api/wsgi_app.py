"""
WSGI entry point with ProxyFix middleware for running behind Traefik reverse proxy
"""
from werkzeug.middleware.proxy_fix import ProxyFix
from entityshape.app import app

# Configure ProxyFix to handle X-Forwarded headers from Traefik
# This fixes URL generation and redirects when behind a reverse proxy
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
    x_prefix=1
)
