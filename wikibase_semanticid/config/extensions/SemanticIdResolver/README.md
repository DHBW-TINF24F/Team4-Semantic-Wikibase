# SemanticIdResolver Extension

This MediaWiki extension provides a special page to resolve Wikibase items and properties by their semantic ID property value and redirect to the entity page.

## Features

- **Special:GoBySemanticId/[id]** - Direct URL access to entities by semantic ID
- **Special:GoBySemanticId?p=[id]** - Query parameter access (recommended for complex IDs)
- Form-based search if no ID is provided in the URL
- Configurable property ID (defaults to P1)
- Searches both items and properties
- Supports multiple semantic ID formats:
  - **IRDI**: `0173-1#02-DAA603#004`
  - **IEC61360-IRDI**: `0112/2///61360_4#AAE186`
  - **URI/URL**: `https://admin-shell-io/semdef/temperature/1/0`
  - **UUID**: `16f642e2-1cb8-4bd5-b605-8577c57fc0e6`
  - **Simple strings**: `foo`, `bar123`

## Usage

### Direct URL Access

#### Simple IDs (path format)
Access an entity with semantic ID "einstein":
```
https://wikibase.local/einstein
```

This automatically redirects to:
```
https://wikibase.local/wiki/Special:GoBySemanticId/einstein
```

You can also use the full Special page URL:
```
https://wikibase.local/wiki/Special:GoBySemanticId/einstein
```

The extension will search both items and properties, and redirect to whichever entity has the matching semantic ID.

#### Complex IDs with Special Characters (query parameter format)

For semantic IDs containing special characters like `#`, `/`, or `:`, use the query parameter format with URL encoding:

**IRDI format** (`0173-1#02-DAA603#004`):
```
https://wikibase.local/?p=0173-1%2302-DAA603%23004
```

**IEC61360-IRDI format** (`0112/2///61360_4#AAE186`):
```
https://wikibase.local/?p=0112%2F2%2F%2F%2F61360_4%23AAE186
```

**URI/URL format** (`https://admin-shell-io/semdef/temperature/1/0`):
```
https://wikibase.local/?p=https%3A%2F%2Fadmin-shell-io%2Fsemdef%2Ftemperature%2F1%2F0
```

**UUID format** (`16f642e2-1cb8-4bd5-b605-8577c57fc0e6`):
```
https://wikibase.local/?p=16f642e2-1cb8-4bd5-b605-8577c57fc0e6
```

Alternatively, you can use the full Special page URL with the query parameter (browser will handle encoding automatically when clicked):
```
https://wikibase.local/wiki/Special:GoBySemanticId?p=0112/2///61360_4#AAE186
```

All formats will:
1. Search for an item or property where property P1 (semantic ID) equals the provided value
2. Redirect to the entity page if found (either item or property page)
3. Show an error message if not found

### Form-Based Search

Navigate to:
```
https://wikibase.local/wiki/Special:GoBySemanticId
```

Enter the semantic ID in the form and submit. The form handles all semantic ID formats automatically.

## Routing

The extension includes Traefik routing configuration that automatically redirects root-level paths to the Special:GoBySemanticId page.

### How It Works

**Simple IDs** - Direct path access:
```
https://semantic-hub.io/einstein
→ Rewrites to: https://semantic-hub.io/wiki/Special:GoBySemanticId/einstein
```

**Complex IDs** - Query parameter access (for IDs with `#`, `/`, `:` characters):
```
https://semantic-hub.io/?p=0112%2F2%2F%2F%2F61360_4%23AAE186
→ Rewrites to: https://semantic-hub.io/wiki/Special:GoBySemanticId?p=0112%2F2%2F%2F%2F61360_4%23AAE186
```

The routing preserves query parameters and handles URL encoding automatically, ensuring all semantic ID formats work correctly.

## Configuration

The property ID used for semantic IDs can be configured in LocalSettings.php:

```php
$wgSemanticIdProperty = 'P1'; // Change to your property ID
```

Default is P1.

## Technical Details

### URL Encoding

When constructing URLs programmatically or sharing links, special characters must be URL-encoded:

- `#` → `%23`
- `/` → `%2F`
- `:` → `%3A`

**Example:** To access an item with semantic ID `0112/2///61360_4#AAE186`, use:
```
https://wikibase.local/?p=0112%2F2%2F%2F%2F61360_4%23AAE186
```

When users click links or submit forms, browsers handle encoding automatically. MediaWiki automatically decodes query parameters before processing.

### Supported Formats

The extension performs exact string matching against the semantic ID property value. Store semantic IDs in your Wikibase items in the exact format you want to search for:

- **IRDI**: `0173-1#02-DAA603#004`
- **IEC61360-IRDI**: `0112/2///61360_4#AAE186`
- **URI**: `https://admin-shell-io/semdef/temperature/1/0`
- **UUID**: `16f642e2-1cb8-4bd5-b605-8577c57fc0e6`
- **Simple strings**: `einstein`, `foo`, `bar123`

## Installation

This extension is already loaded in Wikibase Suite Deploy via `config/Extensions.php`.

To install manually in a standard MediaWiki installation:

1. Copy the extension to `extensions/SemanticIdResolver/`
2. Add to LocalSettings.php:
   ```php
   wfLoadExtension( 'SemanticIdResolver' );
   ```
3. Run update.php (or restart the Wikibase container in Docker)

## Requirements

- MediaWiki >= 1.43.0
- Wikibase extension installed