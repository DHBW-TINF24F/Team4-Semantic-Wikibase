<?php

namespace MediaWiki\Extension\SemanticIdResolver\Specials;

use MediaWiki\SpecialPage\SpecialPage;
use MediaWiki\Title\Title;
use Wikibase\DataModel\Entity\EntityId;
use Wikibase\DataModel\Entity\Item;
use Wikibase\DataModel\Entity\ItemId;
use Wikibase\DataModel\Entity\Property;
use Wikibase\DataModel\Entity\PropertyId;
use Wikibase\Lib\Store\EntityTitleLookup;
use Wikibase\Repo\WikibaseRepo;

/**
 * Special page to resolve items and properties by their semantic ID (P1 property value)
 * and redirect to the entity page.
 *
 * Supports multiple semantic ID formats:
 * - IRDI: 0173-1#02-DAA603#004
 * - IEC61360-IRDI: 0112/2///61360_4#AAE186
 * - URI/URL: https://admin-shell-io/semdef/temperature/1/0
 * - UUID: 16f642e2-1cb8-4bd5-b605-8577c57fc0e6
 *
 * Usage:
 * - Special:GoBySemanticId/foo
 * - Special:GoBySemanticId?p=0173-1#02-DAA603#004
 */
class SpecialGoBySemanticId extends SpecialPage {

	private ?EntityTitleLookup $entityTitleLookup = null;

	public function __construct() {
		parent::__construct( 'GoBySemanticId' );
	}

	/**
	 * @inheritDoc
	 */
	public function execute( $subPage ) {
		$this->setHeaders();
		$this->outputHeader();

		$request = $this->getRequest();
		
		// Support both query parameter (?p=) and URL path formats
		// Query parameter is preferred for complex IDs with special characters
		$semanticId = $request->getText( 'p', '' );
		if ( $semanticId === '' ) {
			$semanticId = $request->getText( 'semanticid', '' );
		}
		if ( $semanticId === '' && $subPage !== null ) {
			$semanticId = trim( $subPage );
		}
		
		// URL decode the semantic ID to handle special characters
		$semanticId = urldecode( $semanticId );

		if ( $semanticId === '' ) {
			$this->showForm();
			return;
		}

		// If semanticId came from form submission (not URL), redirect to clean URL with query parameter
		if ( $request->getText( 'semanticid' ) !== '' && $request->getText( 'p' ) === '' && $subPage === null ) {
			$title = $this->getPageTitle();
			$query = [ 'p' => $semanticId ];
			$this->getOutput()->redirect( $title->getLocalURL( $query ) );
			return;
		}

		// Get the configured property ID for semantic IDs
		$propertyId = $this->getConfig()->get( 'SemanticIdProperty' );

		// Find the entity (item or property) with this semantic ID
		$entityId = $this->findEntityBySemanticId( $semanticId, $propertyId );

		if ( $entityId === null ) {
			$this->getOutput()->addHTML(
				'<div class="error">' .
				$this->msg( 'semanticidresolver-notfound', $semanticId )->escaped() .
				'</div>'
			);
			$this->showForm( $semanticId );
			return;
		}

		// Redirect to the entity page
		$title = $this->getEntityTitleLookup()->getTitleForId( $entityId );
		if ( $title ) {
			$this->getOutput()->redirect( $title->getFullURL() );
		} else {
			$this->getOutput()->addHTML(
				'<div class="error">' .
				$this->msg( 'semanticidresolver-error' )->escaped() .
				'</div>'
			);
		}
	}

	/**
	 * Show the search form
	 *
	 * @param string $defaultValue Default value for the input field
	 */
	private function showForm( string $defaultValue = '' ): void {
		$formDescriptor = [
			'semanticid' => [
				'type' => 'text',
				'name' => 'semanticid',
				'label-message' => 'semanticidresolver-label',
				'default' => $defaultValue,
				'required' => true,
			],
		];

		$htmlForm = \HTMLForm::factory( 'ooui', $formDescriptor, $this->getContext() );
		$htmlForm
			->setMethod( 'get' )
			->setSubmitTextMsg( 'semanticidresolver-submit' )
			->setSubmitCallback( [ $this, 'onSubmit' ] )
			->show();
	}

	/**
	 * Form submit callback (not used, form submits via GET)
	 *
	 * @param array $data
	 * @return bool
	 */
	public function onSubmit( array $data ): bool {
		// This won't be called for GET forms, but is required by HTMLForm
		return false;
	}

	/**
	 * Find an item or property by its semantic ID property value
	 *
	 * @param string $semanticId The semantic ID to search for
	 * @param string $propertyIdString The property ID (e.g., "P1")
	 * @return EntityId|null The entity ID if found, null otherwise
	 */
	private function findEntityBySemanticId( string $semanticId, string $propertyIdString ): ?EntityId {
		try {
			// Parse the property ID using the entity ID parser
			$entityIdParser = WikibaseRepo::getEntityIdParser();
			$propertyId = $entityIdParser->parse( $propertyIdString );
			
			if ( !( $propertyId instanceof PropertyId ) ) {
				wfDebugLog( 'SemanticIdResolver', "Invalid property ID: $propertyIdString" );
				return null;
			}
			
			// Get entity lookup
			$entityLookup = WikibaseRepo::getEntityLookup();
			
			// Use database connection from MediaWiki services
			$services = \MediaWiki\MediaWikiServices::getInstance();
			$dbr = $services->getDBLoadBalancer()->getConnection( DB_REPLICA );
			
			// Get all item and property IDs (search both namespaces 120 and 122)
			$res = $dbr->newSelectQueryBuilder()
				->select( [ 'page_title', 'page_namespace' ] )
				->from( 'page' )
				->where( [
					'page_namespace' => [ 120, 122 ], // Item and Property namespaces
					'page_is_redirect' => 0
				] )
				->limit( 10000 ) // Limit for safety
				->caller( __METHOD__ )
				->fetchResultSet();

			foreach ( $res as $row ) {
				try {
					$entityId = $entityIdParser->parse( $row->page_title );
					
					// Check if it's either an ItemId or PropertyId
					if ( !( $entityId instanceof ItemId ) && !( $entityId instanceof PropertyId ) ) {
						continue;
					}
					
					$entity = $entityLookup->getEntity( $entityId );
					if ( $entity === null ) {
						continue;
					}

					// Check if entity is either Item or Property
					if ( !$entity instanceof Item && !$entity instanceof Property ) {
						continue;
					}

					// Get statements for the semantic ID property
					$statements = $entity->getStatements()->getByPropertyId( $propertyId );
					
					foreach ( $statements as $statement ) {
						$mainSnak = $statement->getMainSnak();
						if ( $mainSnak->getType() === 'value' ) {
							$dataValue = $mainSnak->getDataValue();
							if ( $dataValue->getValue() === $semanticId ) {
								return $entityId;
							}
						}
					}
				} catch ( \Exception $e ) {
					// Skip invalid entities
					wfDebugLog( 'SemanticIdResolver', "Error processing entity {$row->page_title}: " . $e->getMessage() );
					continue;
				}
			}
			
			return null;
		} catch ( \Exception $e ) {
			wfDebugLog( 'SemanticIdResolver', "Fatal error in findEntityBySemanticId: " . $e->getMessage() );
			return null;
		}
	}

	/**
	 * Get the entity title lookup service
	 *
	 * @return EntityTitleLookup
	 */
	private function getEntityTitleLookup(): EntityTitleLookup {
		if ( !isset( $this->entityTitleLookup ) ) {
			$this->entityTitleLookup = WikibaseRepo::getEntityTitleLookup();
		}
		return $this->entityTitleLookup;
	}

	/**
	 * @inheritDoc
	 */
	protected function getGroupName() {
		return 'wikibase';
	}
}
