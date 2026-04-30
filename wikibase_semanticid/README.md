# Wikibase with Semantic ID Routing

This is a customized deployment of [Wikibase Suite Deploy](./README-Wikibase-Suite.md) that adds semantic ID-based routing capabilities to your Wikibase instance. Items and properties can be accessed directly via clean URLs using their semantic identifier (e.g., `https://wikibase.example/einstein` instead of `https://wikibase.example/wiki/Item:Q42`).

## What's Modified

This deployment extends the standard Wikibase Suite Deploy with two custom MediaWiki extensions:

### SemanticIdResolver Extension

Provides URL-based access to items and properties using a semantic ID property.

- Access entities via `Special:GoBySemanticId/{semanticId}`
- Clean URLs via Traefik: `/{semanticId}` redirects to the entity page (item or property)
- Searches both items and properties for matching semantic ID
- Configurable via `SEMANTIC_ID_PROPERTY_ID` environment variable

### UniquePropertyValidator Extension

Ensures data integrity by preventing duplicate values for the semantic ID property.

- Validates uniqueness when creating or editing items and properties
- Automatically enforces uniqueness for the semantic ID property across both items and properties
- Prevents conflicts and ensures reliable URL routing

## System Requirements

### Hardware

- Network connection with a public IP address
- x86_64 (AMD64) architecture
- 8 GB RAM
- 4 GB free disk space

### Software

- Docker 22.0 (or greater)
- Docker Compose 2.10 (or greater)
- git

### Domain Names

You need two DNS records that resolve to your machine's IP address:

- Wikibase (e.g., `wikibase.example`)
- Query Service (e.g., `query.wikibase.example`)

> 💡 **WWW Redirect**: The system automatically redirects `www.{WIKIBASE_PUBLIC_HOST}` to `{WIKIBASE_PUBLIC_HOST}`. If you want to support www URLs, create an additional DNS record for `www.wikibase.example` pointing to the same IP address. SSL certificates will automatically cover both variants.

> 💡 For local testing without public IP, see the [FAQ in the Wikibase Suite README](./README-Wikibase-Suite.md#can-i-host-wbs-deploy-locally).



## Quick Start

### 1. Clone the Repository

Clone the repository including all Git submodules (required for extensions):

```bash
git clone --recurse-submodules https://github.com/foprs/wikibase_semanticid
cd wikibase_semanticid
```

If you already cloned without submodules, initialize them with:

```bash
git submodule update --init --recursive
```

### 2. Configure Environment

Copy the configuration template and customize it:

```bash
cp template.env .env
```

Edit your `.env` file and configure at minimum:

- `WIKIBASE_PUBLIC_HOST` - Your Wikibase domain (e.g., `wikibase.example`)
  - The system automatically handles `www.` redirects if you configure DNS for both variants
- `WDQS_PUBLIC_HOST` - Your Query Service domain
- `MW_ADMIN_NAME` - Administrator username
- `MW_ADMIN_EMAIL` - Administrator email
- `MW_ADMIN_PASS` - Administrator password (min. 10 characters)
- `DB_USER` and `DB_PASS` - Database credentials
- `METADATA_CALLBACK` - Set to `true` or `false`

The `SEMANTIC_ID_PROPERTY_ID` is pre-configured to `P1` (the first property in a new Wikibase instance).

### 3. Start the Services

```bash
docker compose up -d
```

The first start takes several minutes. Check the status with:

```bash
docker ps
```

When ready, the `wbs-deploy-wikibase-1` container will show as `healthy`.

🎉 Access your instance at `https://wikibase.example` (adjust domain accordingly).

### 4. Configure Semantic ID Property

After your Wikibase is running, you need to create the semantic ID property:

1. **Log in** to your Wikibase instance with the admin credentials from your `.env` file

2. **Create a new property**:
   - Navigate to `Special:NewProperty` or click "Create a new property"
   - **Label**: `semanticId` (or your preferred name)
   - **Description**: `Unique semantic identifier for URL-based entity access`
   - **Data type**: `String`
   - Click "Create"

3. **Note the property ID**: After creation, you'll see the property ID in the URL (e.g., `Property:P1`)
   - If this is the first property you created, it will be `P1`
   - If you already had other properties, it might be `P2`, `P3`, etc.

4. **Update configuration** (only if the property ID is NOT P1):
   - Edit your `.env` file
   - Change `SEMANTIC_ID_PROPERTY_ID=P1` to match your property ID
   - Restart the wikibase container:
     ```bash
     docker compose restart wikibase
     ```

### 5. Test Semantic ID Routing

1. **Create a test item** with a semantic ID:
   - Create a new item (e.g., "Albert Einstein")
   - Add a statement with your semantic ID property
   - Set the value to something simple like `einstein`

2. **Access via semantic ID**:
   - Direct access: `https://wikibase.example/einstein`
   - Special page: `https://wikibase.example/wiki/Special:GoBySemanticId/einstein`
   - The system will redirect to the item page

3. **Test with properties** (optional):
   - Edit a property and add a semantic ID statement
   - Access it via the semantic ID URL
   - The system will redirect to the property page

4. **Test uniqueness validation**:
   - Try to create another item or property with the same semantic ID
   - The system should prevent the duplicate and show an error message

## Managing Your Instance

### Stopping the Services

```bash
docker compose stop
```

### Viewing Logs

```bash
docker logs wbs-deploy-wikibase-1
```

### Restarting After Configuration Changes

After editing `.env` or other configuration files:

```bash
docker compose down
docker compose up -d
```

### Backup and Updates

For backup strategies, update procedures, and troubleshooting, refer to the [Wikibase Suite README](./README-Wikibase-Suite.md).

## Advanced Configuration

### Adding More Unique Properties

By default, only the semantic ID property requires unique values. To add more properties that should be unique:

1. Edit `config/Extensions.php`
2. Modify the `$wgUniqueProperties` array:
   ```php
   $wgUniqueProperties = [ 
       getenv( 'SEMANTIC_ID_PROPERTY_ID' ) ?: 'P1',
       'P5',  // Add your additional property IDs
       'P7',
   ];
   ```
3. Restart: `docker compose restart wikibase`

### Adding Other MediaWiki Extensions

To add more extensions to your Wikibase instance, see the [extensions README](./config/extensions/README.md).

### Traefik and URL Routing

The clean URL routing (e.g., `/einstein` → `/wiki/Special:GoBySemanticId/einstein`) is handled by Traefik reverse proxy rules defined in `config/traefik-dynamic.yml`. The configuration excludes standard MediaWiki paths like `/wiki`, `/w`, `/api`, etc.

For more details on customizing the deployment, see the [Wikibase Suite README](./README-Wikibase-Suite.md).

## Architecture

This deployment is built on top of [Wikibase Suite Deploy](https://github.com/wmde/wikibase-release-pipeline) and includes:

- **Wikibase** (MediaWiki + Wikibase extension)
- **MariaDB** (Database)
- **Elasticsearch** (Search functionality)
- **Wikidata Query Service (WDQS)** (SPARQL endpoint)
- **WDQS Frontend** (Query interface)
- **QuickStatements** (Batch editing tool)
- **EntityShape API** (Entity validation backend for EntityShape.js frontend)
- **Traefik** (Reverse proxy with SSL/TLS termination)
- **Custom Extensions** (SemanticIdResolver + UniquePropertyValidator)

For detailed information about each component, see the [Wikibase Suite README](./README-Wikibase-Suite.md).

For details about the EntityShape API integration, see the [EntityShape API README](./entityshape-api/README.md).

## Troubleshooting

### Semantic ID URLs Not Working

- Verify the property was created and you noted the correct property ID
- Check that `SEMANTIC_ID_PROPERTY_ID` in `.env` matches your property ID
- Ensure you restarted the wikibase container after changing `.env`
- Check container logs: `docker logs wbs-deploy-wikibase-1`

### Duplicate Semantic ID Not Blocked

- Verify the UniquePropertyValidator extension is loaded
- Check `docker logs wbs-deploy-wikibase-1` for extension loading messages
- Ensure the property ID in `.env` is correct

### General Issues

For general Wikibase Suite Deploy issues, consult the [Wikibase Suite README](./README-Wikibase-Suite.md) and the [Wikibase documentation](https://www.mediawiki.org/wiki/Wikibase).

## Support

For issues specific to the semantic ID extensions:
- Check the [extensions documentation](./config/extensions/README.md)
- Review extension code in `config/extensions/SemanticIdResolver/` and `config/extensions/UniquePropertyValidator/`

For general Wikibase Suite Deploy issues:
- See the [Wikibase Suite README](./README-Wikibase-Suite.md)
- Visit the [Wikibase Community](https://www.mediawiki.org/wiki/Wikibase)

## Contributing

### Development Workflow

To maintain stability and ensure proper deployment, the following workflow must be observed:

- **No direct commits to main**: Direct commits to the `main` branch are disabled. All changes must be submitted via pull requests.
- **Automatic deployment**: When a pull request is merged into `main`, the changes are automatically deployed to the production server. This triggers a complete recreation and restart of the container stack.
- **Testing before merge**: Please ensure that your branch has been thoroughly tested and is working correctly before merging into `main`. Once merged, the changes will go live immediately.

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes and test them locally
3. Submit a pull request with a clear description of the changes
4. Once approved and merged, your changes will be deployed automatically

## License

This deployment configuration and custom extensions are provided as-is. 

The custom extensions (SemanticIdResolver and UniquePropertyValidator) are currently proprietary software. FoP Consult GmbH reserves all rights regarding the use, distribution, modification, and other exploitation of these extensions. This licensing may be subject to change in the future.

The underlying Wikibase Suite components are licensed under their respective licenses. See the [Wikibase Suite repository](https://github.com/wmde/wikibase-release-pipeline) for details.