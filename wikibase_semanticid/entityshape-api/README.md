# EntityShape API Integration

This directory contains the Docker integration for the [EntityShape API](https://github.com/EntitySchema/entityshape), a Python-based backend service that validates Wikibase entities against EntitySchema definitions.

## Purpose

The EntityShape API is integrated into this Wikibase deployment to provide a validation endpoint for the EntityShape.js frontend script. This allows users to validate entities in real-time against EntitySchema definitions directly within the Wikibase interface.

## Integration Architecture

The API is containerized and integrated into the Docker Compose stack as the `entityshape-api` service. It runs behind the Traefik reverse proxy and is accessible at a configurable subpath (default: `/entityshape`).

### Components

- **`entityshape/`** - Git submodule containing the original EntityShape API repository
- **`Dockerfile`** - Container definition using Python 3.11-slim and Gunicorn WSGI server
- **`patch_urls.py`** - Build-time script that replaces hardcoded Wikidata URLs with internal Wikibase URLs
- **`wsgi_app.py`** - WSGI wrapper adding ProxyFix middleware for proper URL generation behind the reverse proxy

### How It Works

1. **Docker Build Process**:
   - Copies the EntityShape API code from the submodule
   - Runs `patch_urls.py` to replace `https://www.wikidata.org` with `http://wikibase`
   - Installs dependencies and configures Gunicorn with 4 workers

2. **Runtime**:
   - API runs on internal port 8000
   - Traefik routes external requests from `https://{WIKIBASE_PUBLIC_HOST}/entityshape/*` to the container
   - ProxyFix middleware handles X-Forwarded headers for correct redirect URL generation
   - Service communicates with Wikibase via Docker internal network DNS

3. **URL Patching**:
   - During Docker build, all hardcoded Wikidata.org URLs in the API code are replaced with `http://wikibase`
   - This allows the API to fetch entity and schema data from the local Wikibase instance instead of Wikidata

## Configuration

### Environment Variables

Configure the API path in your `.env` file:

```env
ENTITYSHAPE_PATH=/entityshape
```

This variable determines the URL path where the API will be accessible:
- API v2 endpoint: `https://{WIKIBASE_PUBLIC_HOST}/entityshape/api/v2`
- API v1 endpoint: `https://{WIKIBASE_PUBLIC_HOST}/entityshape/api`

### Traefik Routing

The Traefik configuration in `config/traefik-dynamic.yml` handles:
- Path-based routing with prefix matching
- StripPrefix middleware to remove `/entityshape` before forwarding to the container
- X-Forwarded-Prefix header injection for proper URL generation
- CORS headers for cross-origin requests
- SSL termination

## API Endpoints

### v2 API (Recommended)

```
GET /entityshape/api/v2?entityschema={SCHEMA_ID}&entity={ENTITY_ID}&language={LANG}
```

**Example:**
```bash
curl "https://wikibase.example/entityshape/api/v2?entityschema=E1&entity=Q42&language=en"
```

**Response:** JSON with validation results including property checks and schema compliance

### v1 API

```
GET /entityshape/api?entityschema={SCHEMA_ID}&entity={ENTITY_ID}&language={LANG}
```

## Integration with EntityShape.js Frontend

The EntityShape.js frontend script can be configured to use this API endpoint for real-time validation. Update the frontend configuration to point to:

```
https://{WIKIBASE_PUBLIC_HOST}/entityshape/api/v2
```

This allows the frontend to validate entities against schemas without relying on external services.

## Docker Compose Service

The service is defined in `docker-compose.yml` with:
- Build context pointing to this directory
- Dependency on the `wikibase` service health check
- Health check on the API's `/api/v2` endpoint
- Automatic restart policy

## Development and Updates

### Updating the EntityShape API

The EntityShape API is included as a git submodule. To update to a newer version:

```bash
cd entityshape-api/entityshape
git fetch
git checkout <new-version-or-branch>
cd ../..
git add entityshape-api/entityshape
git commit -m "Update EntityShape API to <version>"
```

After updating, rebuild the container:

```bash
docker compose build entityshape-api
docker compose up -d entityshape-api
```

### Testing the API

Test if the API is responding:

```bash
curl -k "https://wikibase.example/entityshape/api/v2?entityschema=E1&entity=Q1&language=en"
```

Check if the container can reach Wikibase:

```bash
docker exec wbs-deploy-entityshape-api-1 python -c "import urllib.request; import json; response = urllib.request.urlopen('http://wikibase/w/api.php?action=query&meta=siteinfo&format=json'); data = json.loads(response.read()); print('Wikibase accessible:', 'query' in data)"
```

## Troubleshooting

### API Not Responding

1. Check container status: `docker ps | grep entityshape-api`
2. View container logs: `docker logs wbs-deploy-entityshape-api-1`
3. Verify Traefik routing: `docker logs wbs-deploy-traefik-1`

### URL Routing Issues

- Ensure `ENTITYSHAPE_PATH` in `.env` matches the Traefik configuration
- Verify the path doesn't conflict with other routes
- Check that Traefik has the environment variable: `docker exec wbs-deploy-traefik-1 env | grep ENTITYSHAPE`

### Entity/Schema Data Not Loading

- Verify the wikibase service is healthy: `docker ps`
- Test internal connectivity from the API container (see Testing section above)
- Check if entities and schemas exist in your Wikibase instance

## License

The EntityShape API integration components in this directory are part of the Wikibase SemanticID deployment.

The original EntityShape API code (in the `entityshape/` submodule) is licensed under its own terms. See the [EntityShape repository](https://github.com/EntitySchema/entityshape) for details.
