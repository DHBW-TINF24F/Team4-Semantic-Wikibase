<?php
// ************************************************************************
// Wikibase Suite Deploy Extension.php
// ************************************************************************
//
// File to load MediaWiki extensions.
//
// This file will be loaded after all other extensions have been loaded,
// just like as if this code would be at the end of LocalSettings.php.
//
// Make sure to prefix the extensions name with "extensions/" when loading.
// e.g. when extension installation instructions state you need to put
//   wfLoadExtension( 'WikibaseLexeme' );
// here in Wikibase Suite Deploy you need to put
//   wfLoadExtension( 'extensions/WikibaseLexeme' );

// ========================================================================
// SemanticIdResolver Extension
// ========================================================================
// Provides a special page to access items and properties by their semantic ID property.
// URL: Special:GoBySemanticId/{semanticId}
// Clean URL via Traefik: /{semanticId}
//
// SETUP: After creating your "semanticId" property in Wikibase, update 
// the SEMANTIC_ID_PROPERTY_ID environment variable in your .env file.
// Default is P1 (the first property created in a new Wikibase instance).
//
// The extension searches both items and properties for the semantic ID value
// and redirects to whichever entity (item or property) has the matching value.
wfLoadExtension( 'extensions/SemanticIdResolver' );
$wgSemanticIdProperty = getenv( 'SEMANTIC_ID_PROPERTY_ID' ) ?: 'P1';

// ========================================================================
// UniquePropertyValidator Extension
// ========================================================================
// Prevents duplicate values for specified properties across all items and properties.
// Configure which properties should have unique values.
//
// DEFAULT: Only the semanticId property is validated for uniqueness.
// The property ID is read from SEMANTIC_ID_PROPERTY_ID environment variable.
// This ensures semantic IDs are unique across both items AND properties.
wfLoadExtension( 'extensions/UniquePropertyValidator' );
$wgUniqueProperties = [ getenv( 'SEMANTIC_ID_PROPERTY_ID' ) ?: 'P1' ];

// ========================================================================
// QualifierConfirmation Extension
// ========================================================================
// Shows a client-side confirmation dialog when a user saves a Wikibase statement
// that carries a qualifier whose property+value matches a configured rule.
//
// DEFAULT: One rule is configured – any statement whose qualifier property
// QUALIFIER_CONFIRMATION_PROPERTY has the value QUALIFIER_CONFIRMATION_VALUE
// will prompt the user with QUALIFIER_CONFIRMATION_MESSAGE before saving.
wfLoadExtension( 'extensions/QualifierConfirmation' );
$wgQualifierConfirmationRules = [
    [
        'qualifierProperty'   => getenv( 'QUALIFIER_CONFIRMATION_PROPERTY' ) ?: 'P24',
        'qualifierValue'      => getenv( 'QUALIFIER_CONFIRMATION_VALUE' )    ?: 'yes',
        'confirmationMessage' => getenv( 'QUALIFIER_CONFIRMATION_MESSAGE' )  ?:
            'This property has been standardized by a standardization body.' .
            ' Please confirm, that your change is fully compliant to that external definition.',
    ],
];

// ========================================================================
// Third-Party Extensions
// ========================================================================
wfLoadExtension( 'EntitySchema' );

// ========================================================================
// Pre-defined Additional Configuration
// ========================================================================

// Disable access to Action API for anonymous users
$wgHooks['ApiCheckCanExecute'][] = function ( $module, $user, &$message ) {
    $permissionManager = \MediaWiki\MediaWikiServices::getInstance()->getPermissionManager();

    // Only users with "api" right can use API modules
    if ( !$permissionManager->userHasRight( $user, 'api' ) ) {
        $message = 'apierror-api-permission-required';
        return false;
    }

    return true;
};
$wgGroupPermissions['user']['api'] = true;       // Registered users allowed
$wgGroupPermissions['sysop']['api'] = true;      // Sysops allowed
$wgGroupPermissions['bot']['api'] = true;        // Bots allowed
// ========================================================================
// InputBox Extension for custom search fields
// ========================================================================
wfLoadExtension( 'InputBox' );


$wgRawHtml = true;

