FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY entityshape/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY entityshape/ .

# Copy WSGI wrapper with ProxyFix middleware (outside submodule)
COPY wsgi_app.py .

# Copy and run monkey-patch script to replace hardcoded Wikidata URLs
COPY patch_urls.py /tmp/patch_urls.py
RUN python /tmp/patch_urls.py && rm /tmp/patch_urls.py

# Expose port for Gunicorn
EXPOSE 8000

# Use Gunicorn as production WSGI server (not Flask dev server)
# 4 workers for handling concurrent requests
# Use wsgi_app.py which includes ProxyFix middleware for proper URL generation behind Traefik
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi_app:app"]