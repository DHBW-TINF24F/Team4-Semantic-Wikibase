<?php

namespace MediaWiki\Extension\UniquePropertyValidator;

use ApiBase;
use MediaWiki\MediaWikiServices;
use Wikibase\DataModel\Entity\Item;
use Wikibase\DataModel\Entity\ItemId;
use Wikibase\DataModel\Entity\Property;
use Wikibase\DataModel\Entity\PropertyId;
use Wikibase\Repo\WikibaseRepo;

class Hooks {

	/**
	 * Hook handler for ApiCheckCanExecute
	 * Validates entity edits before they are executed
	 *
	 * @param ApiBase $module
	 * @param \User $user
	 * @param array|string|null &$message
	 * @return bool
	 */
	public static function onApiCheckCanExecute( $module, $user, &$message ) {
		$moduleName = $module->getModuleName();
		\wfDebugLog( 'UniquePropertyValidator', 'ApiCheckCanExecute called for module: ' . $moduleName );

		// Process both wbeditentity and wbsetclaim modules
		if ( $moduleName !== 'wbeditentity' && $moduleName !== 'wbsetclaim' ) {
			return true;
		}

		\wfDebugLog( 'UniquePropertyValidator', 'Processing Wikibase edit module: ' . $moduleName );

		$request = $module->getRequest();
		
		// Handle wbsetclaim differently than wbeditentity
		if ( $moduleName === 'wbsetclaim' ) {
			return self::validateSetClaim( $request, $message );
		}
		
		// Handle wbeditentity
		return self::validateEditEntity( $request, $message );
	}

	/**
	 * Validate a wbsetclaim API call
	 *
	 * @param \WebRequest $request
	 * @param array|string|null &$message
	 * @return bool
	 */
	private static function validateSetClaim( $request, &$message ) {
		$config = MediaWikiServices::getInstance()->getMainConfig();
		$uniqueProperties = $config->get( 'UniqueProperties' );

		if ( empty( $uniqueProperties ) ) {
			return true;
		}

		// Get the claim data
		$claim = $request->getVal( 'claim' );
		if ( !$claim ) {
			\wfDebugLog( 'UniquePropertyValidator', 'No claim parameter' );
			return true;
		}

		$claimData = json_decode( $claim, true );
		if ( !$claimData || !isset( $claimData['mainsnak'] ) ) {
			\wfDebugLog( 'UniquePropertyValidator', 'Invalid claim data' );
			return true;
		}

		// Get property ID from the claim
		$propertyId = $claimData['mainsnak']['property'] ?? null;
		if ( !$propertyId ) {
			return true;
		}

		// Check if this property should be unique
		if ( !in_array( $propertyId, $uniqueProperties ) ) {
			\wfDebugLog( 'UniquePropertyValidator', "Property $propertyId is not in unique list" );
			return true;
		}

		\wfDebugLog( 'UniquePropertyValidator', "Checking unique property: $propertyId" );

		// Get the value from the claim
		if ( !isset( $claimData['mainsnak']['datavalue']['value'] ) ) {
			return true;
		}

		$value = $claimData['mainsnak']['datavalue']['value'];
		
		// Handle different value types
		if ( is_array( $value ) && isset( $value['text'] ) ) {
			$searchValue = $value['text'];
		} elseif ( is_string( $value ) ) {
			$searchValue = $value;
		} else {
			$searchValue = json_encode( $value );
		}

		\wfDebugLog( 'UniquePropertyValidator', "Value to check: $searchValue" );

		// Get the entity ID being edited from the claim GUID
		// In wbsetclaim, the entity is identified by the claim GUID (e.g. "Q18$guid-here")
		$entityId = null;
		if ( isset( $claimData['id'] ) ) {
			$parts = explode( '$', $claimData['id'], 2 );
			if ( count( $parts ) === 2 ) {
				$entityId = $parts[0];
			}
		}
		// Fall back to explicit entity parameter if available
		if ( !$entityId ) {
			$entityId = $request->getVal( 'entity' );
		}
		
		try {
			// Parse the property ID properly
			$propertyIdObj = WikibaseRepo::getEntityIdParser()->parse( $propertyId );
			
			if ( !$propertyIdObj instanceof PropertyId ) {
				\wfLogWarning( "Invalid property ID format: $propertyId" );
				return true;
			}
			
			$duplicateEntityId = self::findDuplicateValue( $propertyIdObj, $searchValue, $entityId );

			if ( $duplicateEntityId ) {
				\wfDebugLog( 'UniquePropertyValidator', "Duplicate found on: $duplicateEntityId" );
				
				$message = [
					'uniquepropertyvalidator-duplicate-value',
					$propertyId,
					$searchValue,
					$duplicateEntityId
				];
				return false;
			}
		} catch ( \Exception $e ) {
			\wfLogWarning( "Error validating unique property: " . $e->getMessage() );
		}

		\wfDebugLog( 'UniquePropertyValidator', 'Validation passed for wbsetclaim' );
		return true;
	}

	/**
	 * Validate a wbeditentity API call
	 *
	 * @param \WebRequest $request
	 * @param array|string|null &$message
	 * @return bool
	 */
	private static function validateEditEntity( $request, &$message ) {
		
		// Get the data being submitted
		$data = $request->getVal( 'data' );
		if ( !$data ) {
			\wfDebugLog( 'UniquePropertyValidator', 'No data parameter found' );
			return true;
		}

		$entityData = json_decode( $data, true );
		if ( !$entityData || !isset( $entityData['claims'] ) ) {
			\wfDebugLog( 'UniquePropertyValidator', 'No claims in data' );
			return true;
		}

		\wfDebugLog( 'UniquePropertyValidator', 'Processing claims: ' . json_encode( array_keys( $entityData['claims'] ) ) );

		$config = MediaWikiServices::getInstance()->getMainConfig();
		$uniqueProperties = $config->get( 'UniqueProperties' );

		if ( empty( $uniqueProperties ) ) {
			\wfDebugLog( 'UniquePropertyValidator', 'No unique properties configured' );
			return true;
		}

		// Get the item ID being edited (if it exists)
		$itemIdString = $request->getVal( 'id' );
		$currentEntityId = $itemIdString ?: null;

		\wfDebugLog( 'UniquePropertyValidator', 'Checking entity: ' . ( $currentEntityId ?? 'new entity' ) );

		// Check each unique property
		foreach ( $uniqueProperties as $propertyIdString ) {
			if ( !isset( $entityData['claims'][$propertyIdString] ) ) {
				continue;
			}

			\wfDebugLog( 'UniquePropertyValidator', "Found claims for property $propertyIdString" );

			$claims = $entityData['claims'][$propertyIdString];
			
			foreach ( $claims as $claim ) {
				if ( !isset( $claim['mainsnak']['datavalue']['value'] ) ) {
					continue;
				}

				$value = $claim['mainsnak']['datavalue']['value'];
				
				// Handle different value types
				if ( is_array( $value ) && isset( $value['text'] ) ) {
					$searchValue = $value['text'];
				} elseif ( is_string( $value ) ) {
					$searchValue = $value;
				} else {
					$searchValue = json_encode( $value );
				}

				\wfDebugLog( 'UniquePropertyValidator', "Checking property $propertyIdString with value: $searchValue" );

				try {
					// Parse the property ID properly
					$propertyId = WikibaseRepo::getEntityIdParser()->parse( $propertyIdString );
					
					if ( !$propertyId instanceof PropertyId ) {
						\wfLogWarning( "Invalid property ID format: $propertyIdString" );
						continue;
					}
					
					$duplicateEntityId = self::findDuplicateValue( $propertyId, $searchValue, $currentEntityId );

					if ( $duplicateEntityId ) {
						\wfDebugLog( 'UniquePropertyValidator', "Duplicate found: $duplicateEntityId" );
						
						// Set the error message
						$message = [
							'uniquepropertyvalidator-duplicate-value',
							$propertyIdString,
							$searchValue,
							$duplicateEntityId
						];
						return false;
					}
				} catch ( \Exception $e ) {
					\wfLogWarning( "Error validating unique property: " . $e->getMessage() );
				}
			}
		}

		\wfDebugLog( 'UniquePropertyValidator', 'Validation passed' );
		return true;
	}

	/**
	 * Find if a property value exists on another item or property
	 *
	 * @param PropertyId $propertyId
	 * @param mixed $value
	 * @param string|null $excludeEntityId Entity ID to exclude from search (the current entity being edited)
	 * @return string|null Entity ID if duplicate found, null otherwise
	 */
	private static function findDuplicateValue( PropertyId $propertyId, $value, $excludeEntityId ) {
		$dbr = MediaWikiServices::getInstance()->getDBLoadBalancer()->getConnection( DB_REPLICA );
		
		// Query for both items (namespace 120) and properties (namespace 122)
		$result = $dbr->newSelectQueryBuilder()
			->select( [ 'page_title', 'page_namespace', 'page_content_model' ] )
			->from( 'page' )
			->where( [
				'page_namespace' => [ 120, 122 ], // Wikibase item and property namespaces
			] )
			->limit( 10000 )
			->caller( __METHOD__ )
			->fetchResultSet();

		$entityLookup = WikibaseRepo::getEntityLookup();
		$entityIdParser = WikibaseRepo::getEntityIdParser();
		$searchValue = self::normalizeValue( $value );

		foreach ( $result as $row ) {
			$entityIdString = $row->page_title;

			// Skip the entity we're currently editing
			if ( $excludeEntityId && $entityIdString === $excludeEntityId ) {
				continue;
			}

			try {
				// Parse entity ID (works for both items and properties)
				$entityId = $entityIdParser->parse( $entityIdString );
				$entity = $entityLookup->getEntity( $entityId );

				// Check if entity is either an Item or a Property
				if ( !$entity instanceof Item && !$entity instanceof Property ) {
					continue;
				}

				// Check if this entity has the property with the same value
				$statements = $entity->getStatements()->getByPropertyId( $propertyId );

				foreach ( $statements as $statement ) {
					$mainSnak = $statement->getMainSnak();

					if ( !$mainSnak instanceof \Wikibase\DataModel\Snak\PropertyValueSnak ) {
						continue;
					}

					$entityValue = $mainSnak->getDataValue()->getValue();
					$normalizedEntityValue = self::normalizeValue( $entityValue );

					if ( $normalizedEntityValue === $searchValue ) {
						return $entityIdString;
					}
				}
			} catch ( \Exception $e ) {
				// Skip entities that can't be loaded
				continue;
			}
		}

		return null;
	}

	/**
	 * Normalize a value for comparison
	 *
	 * @param mixed $value
	 * @return string
	 */
	private static function normalizeValue( $value ) {
		if ( is_string( $value ) ) {
			return $value;
		} elseif ( is_object( $value ) && method_exists( $value, 'getValue' ) ) {
			return (string)$value->getValue();
		} elseif ( is_object( $value ) && method_exists( $value, '__toString' ) ) {
			return (string)$value;
		}
		
		return (string)$value;
	}

	/**
	 * Format a value for display in error messages
	 *
	 * @param mixed $value
	 * @return string
	 */
	private static function formatValue( $value ) {
		return self::normalizeValue( $value );
	}
}
