# Wikibase Suite User Defined MediaWiki Extensions

This directory contains custom MediaWiki/Wikibase extensions. This deployment includes two pre-configured extensions for semantic ID routing and validation.

> 💡 For initial setup and usage instructions, see the [main README](../../README.md).

## Included Custom Extensions

### SemanticIdResolver (`SemanticIdResolver/`)

Provides URL-based access to items and properties using a semantic ID property.

**Features:**
- Special page `Special:GoBySemanticId/{semanticId}` for direct entity access
- Searches for both items and properties by semantic ID value
- Redirects to the appropriate entity page when found (item or property)
- Shows helpful error messages when not found

**Technical Details:**
- Extends `SpecialPage` class
- Uses MediaWiki database API to query claims across both item (namespace 120) and property (namespace 122) namespaces
- Property ID configured via `SEMANTIC_ID_PROPERTY_ID` environment variable
- Fallback to `P1` if environment variable not set

**URL Routing:**
Clean URLs (e.g., `/{semanticId}`) are handled by Traefik reverse proxy configuration in `../traefik-dynamic.yml`.

### UniquePropertyValidator (`UniquePropertyValidator/`)

Prevents duplicate values for specified properties across all items and properties.

**Features:**
- Validates uniqueness when creating or editing items and properties
- Intercepts API calls to prevent duplicate values
- Supports both `wbsetclaim` and `wbeditentity` API modules
- Returns user-friendly error messages
- Ensures semantic IDs remain unique across both items and properties

**Technical Details:**
- Hooks into `ApiCheckCanExecute` to intercept Wikibase API calls
- Queries database to check for existing values in both item (namespace 120) and property (namespace 122) namespaces
- Property ID configured via `SEMANTIC_ID_PROPERTY_ID` environment variable
- Configurable for multiple properties via `$wgUniqueProperties` array

**Configuration:**
By default, only the semantic ID property is validated. To add more properties:

```php
// In ../Extensions.php
$wgUniqueProperties = [ 
    getenv( 'SEMANTIC_ID_PROPERTY_ID' ) ?: 'P1',
    'P5',  // Add your property IDs here
    'P7',
];
```

### QualifierConfirmation (`QualifierConfirmation/`)

Shows a client-side confirmation dialog when a user saves a Wikibase statement that carries a qualifier whose property and value match a configured rule.

**Features:**
- Intercepts the statement save button click in the Wikibase UI (capture phase)
- Checks all qualifiers on the statement being saved against a list of rules
- Shows an OO.ui confirm/cancel dialog with a configurable message before proceeding
- Rule list is configurable via `Extensions.php` / environment variables
- Supports multiple rules
- Client-side only — does not block direct API access

**Technical Details:**
- PHP `BeforePageDisplay` hook injects the rule list into `mw.config` as `wgQualifierConfirmationRules` and loads the ResourceLoader module on Wikibase entity pages (namespaces 120 and 122)
- JavaScript reads the qualifier property IDs and values from the Wikibase `snakview` jQuery widget (`.data('snakview').snak()`) for reliable comparison against configured rules
- Uses OOUI's built-in `OO.ui.confirm()` for the dialog; OK/Cancel button labels are provided by OOUI's own i18n

**Configuration:**
Rules are configured in `../Extensions.php`. Each rule contains a qualifier property ID, a target value, and the message to display:

```php
// In ../Extensions.php
$wgQualifierConfirmationRules = [
    [
        'qualifierProperty'   => getenv( 'QUALIFIER_CONFIRMATION_PROPERTY' ) ?: 'P24',
        'qualifierValue'      => getenv( 'QUALIFIER_CONFIRMATION_VALUE' )    ?: 'Q7',
        'confirmationMessage' => getenv( 'QUALIFIER_CONFIRMATION_MESSAGE' )  ?:
            'This property has been standardized by a standardization body.' .
            ' Please confirm, that your change is fully compliant to that external definition.',
    ],
    // Add more rules here if needed
];
```

The three values are read from environment variables (see `../../template.env`):

| Variable | Description | Example |
|---|---|---|
| `QUALIFIER_CONFIRMATION_PROPERTY` | Property ID of the qualifier to watch | `P24` |
| `QUALIFIER_CONFIRMATION_VALUE` | Exact qualifier value that triggers the dialog | `yes` |
| `QUALIFIER_CONFIRMATION_MESSAGE` | Message shown in the confirm dialog | *(see template.env)* |

---

## Automated Dependency Installation

This deployment includes an automated system for installing Composer dependencies required by MediaWiki extensions.

### How It Works

When you start the Wikibase stack with `docker compose up`, an **init container** runs first to check all extensions for Composer dependencies:

1. The `extension-installer` service scans the `config/extensions/` directory
2. For each extension with a `composer.json` file, it checks if dependencies are already installed
3. If the `vendor/` directory doesn't exist, it runs `composer install --no-dev`
4. Once complete, the Wikibase service starts with all dependencies ready

### The Install Script

The automation is handled by `install.sh` in this directory. The script:

- ✅ **Is idempotent** - Only installs if `vendor/` doesn't exist
- ✅ **Handles multiple extensions** - Processes all extensions automatically
- ✅ **Provides clear output** - Shows which extensions were processed
- ✅ **Fails safely** - Stops startup if dependency installation fails

### When Dependencies Are Installed

Dependencies are installed automatically:
- On first `docker compose up` after adding an extension
- After running `docker compose down -v` (which removes volumes)
- When you delete a `vendor/` directory manually

### Version Control

The `vendor/` directories are excluded from Git (via `.gitignore`). This means:
- ✅ Repository stays clean and lightweight
- ✅ Each environment installs dependencies on-demand
- ✅ No version conflicts between different operating systems
- ✅ Students get fresh, working dependencies

### Troubleshooting

If you encounter issues with extension dependencies:

1. **Check the logs:**
   ```bash
   docker compose logs extension-installer
   ```

2. **Force reinstallation:**
   ```bash
   # Stop services
   docker compose down
   
   # Remove vendor directory for specific extension
   rm -rf config/extensions/EntitySchema/vendor
   
   # Restart
   docker compose up
   ```

3. **Verify installation:**
   ```bash
   # Check that vendor directory was created
   ls -la config/extensions/EntitySchema/vendor
   ```

## Extension Configuration

Extensions are loaded via `../Extensions.php`, which is mounted into the container at `/var/www/html/LocalSettings.d/90_UserDefinedExtensions.php`.

Current configuration:
```php
// Load extensions
wfLoadExtension( 'extensions/SemanticIdResolver' );
wfLoadExtension( 'extensions/UniquePropertyValidator' );
wfLoadExtension( 'extensions/QualifierConfirmation' );

// Configure semantic ID property
$wgSemanticIdProperty = getenv( 'SEMANTIC_ID_PROPERTY_ID' ) ?: 'P1';
$wgUniqueProperties = [ getenv( 'SEMANTIC_ID_PROPERTY_ID' ) ?: 'P1' ];

// Configure qualifier confirmation rules
$wgQualifierConfirmationRules = [
    [
        'qualifierProperty'   => getenv( 'QUALIFIER_CONFIRMATION_PROPERTY' ) ?: 'P24',
        'qualifierValue'      => getenv( 'QUALIFIER_CONFIRMATION_VALUE' )    ?: 'yes',
        'confirmationMessage' => getenv( 'QUALIFIER_CONFIRMATION_MESSAGE' )  ?: '...',
    ],
];
```

---

## Adding Additional Extensions

You can add more MediaWiki/Wikibase extensions beyond the included ones. The process involves three steps:

1. **Download and extract** the extension to this directory
2. **Load the extension** via `../Extensions.php`
3. **Restart** the stack

**Note:** If the extension requires Composer dependencies, they will be installed automatically on the next `docker compose up`.

### 1. Downloading Extensions

In order to download additional MediaWiki extensions, you can visit e.g. https://www.mediawiki.org/wiki/Special:ExtensionDistributor. Select the extension to download. Next, select the MediaWiki version your extension needs to be compatible with. You can find out what MediaWiki Version you are running by visiting https://wikibase.example/wiki/Special:Version (replace the domain name with yours).

Once the file is downloaded, unpack it to `config/extensions`

```
deploy
|
+- config
   |
   +- extensions
      |
      +- README.md <- you are here
      |
      +- MyExtension <- we are going to create this directory

```

```sh
tar -xzf MyExtension.tar.gz -C path/to/deploy/config/extensions
```

Verify that you created `deploy/config/extensions/MyExtension` and that this directory contains an `extension.json` file.

### 2. Loading the Extension

Follow the installation instructions for your extension. In most cases, you just need to add one line to `../Extensions.php`:

```php
wfLoadExtension('extensions/MyExtension');
```

**Important:** Make sure to prefix the extension name with `extensions/` as shown above.

Some extensions may require additional configuration. Refer to the extension's documentation for details.

### 3. Restarting the Stack

After adding the extension, restart the entire stack to trigger dependency installation and extension loading:

```bash
# Stop all services
docker compose down

# Start all services (will install dependencies if needed)
docker compose up -d
```

The `extension-installer` init container will automatically detect if your new extension has a `composer.json` file and install its dependencies before Wikibase starts.

**Note:** Some extensions require running `update.php` to update the database schema. The Wikibase Suite Deploy image runs this automatically on container startup, so no manual action is needed.

### 4. Verify Installation

Verify that your extension was loaded successfully:

1. Visit `https://wikibase.example/wiki/Special:Version` (adjust domain)
2. Find your extension in the "Installed extensions" section

## Extension Maintenance

### Updating Extensions

When you install extensions manually as described above, you are responsible to update those extensions. Extensions might contain security vulnerabilities that eventually get patches. You are responsible to install these patches! When you upgrade a MediaWiki minor version, e.g. from 1.42 to 1.43 (this can happen with Wikibase Suite Deploy major version updates), the extension might need an update too in order to remain compatible.

## More information

More information are available in the [MediaWiki Manual](https://www.mediawiki.org/wiki/Manual:Extensions).
