# UniquePropertyValidator Extension

This MediaWiki extension ensures that specified Wikibase properties have unique values across all items and properties.

## Features

- Validates property uniqueness before saving items and properties
- Prevents duplicate values for configured properties across both items and properties
- Shows clear error messages indicating which entity already has the value
- Configurable list of properties to validate

## Configuration

Add the extension to your `Extensions.php`:

```php
wfLoadExtension('extensions/UniquePropertyValidator');
```

Configure which properties should be unique in `LocalSettings.php`:

```php
$wgUniqueProperties = ['P1', 'P2']; // Default is ['P1']
```

## Usage

When a user tries to save an item or property with a property value that already exists on another entity, they will see an error message:

> The value "example" for property P1 already exists on entity [[Q123]]. This property requires unique values.

The save will be blocked until the duplicate is resolved. The entity reference will link to either an item (Q-number) or property (P-number), depending on which entity already has the value.

## How It Works

The extension hooks into the `ApiCheckCanExecute` hook, which fires before content is saved. It:

1. Checks if the content being saved is a Wikibase Item or Property
2. Iterates through all configured unique properties
3. For each property value in the entity, searches all other items and properties for the same value
4. If a duplicate is found, blocks the save and shows an error message

## Performance Considerations

For large Wikibase instances, the uniqueness check queries all items and properties. Consider these optimizations:

- Keep the list of unique properties minimal
- Consider adding database indices for frequently checked properties
- For very large instances, you may want to implement caching or a dedicated uniqueness index table
