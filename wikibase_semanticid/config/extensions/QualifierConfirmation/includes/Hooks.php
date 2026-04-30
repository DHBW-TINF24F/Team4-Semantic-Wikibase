<?php

namespace MediaWiki\Extension\QualifierConfirmation;

use MediaWiki\MediaWikiServices;
use OutputPage;
use Skin;

class Hooks {

	/**
	 * Hook handler for BeforePageDisplay
	 * Injects the qualifier confirmation rules and JS module into Wikibase entity pages.
	 *
	 * @param OutputPage $out
	 * @param Skin $skin
	 */
	public static function onBeforePageDisplay( OutputPage $out, Skin $skin ): void {
		$title = $out->getTitle();

		// Only inject on Wikibase item (NS 120) and property (NS 122) pages
		if ( !$title || !in_array( $title->getNamespace(), [ 120, 122 ] ) ) {
			return;
		}

		$config = MediaWikiServices::getInstance()->getMainConfig();
		$rules = $config->get( 'QualifierConfirmationRules' );

		if ( empty( $rules ) ) {
			return;
		}

		// Pass rules to JavaScript via mw.config
		$out->addJsConfigVars( 'wgQualifierConfirmationRules', $rules );

		// Load the confirmation module
		$out->addModules( 'ext.qualifierconfirmation' );
	}
}
