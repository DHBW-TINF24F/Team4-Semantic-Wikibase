/**
 * QualifierConfirmation – client-side confirmation dialog for standardized qualifier values.
 *
 * Intercepts the `wbsetclaim` MediaWiki API call and checks whether the claim's qualifiers
 * include a property+value pair that matches a configured rule. If so, an OO.ui.confirm
 * dialog is shown before the save proceeds. The user must click "OK" to confirm or
 * "Cancel" to abort.
 *
 * Configuration is injected by the PHP Hooks::onBeforePageDisplay into mw.config as
 * 'wgQualifierConfirmationRules', which is an array of objects:
 *   { qualifierProperty: 'P3', qualifierValue: 'yes', confirmationMessage: '...' }
 *
 * The approach patches mw.Api.prototype.post so it works regardless of which Wikibase
 * UI component triggers the save (inline editor, qualifier popup, etc.).
 */
( function () {
	'use strict';

	console.log( '[QualifierConfirmation] Script executing' );

	mw.loader.using( [ 'mediawiki.api', 'oojs-ui-windows' ] ).done( function () {
		var rules = mw.config.get( 'wgQualifierConfirmationRules' );

		console.log( '[QualifierConfirmation] Loaded. Rules:', JSON.stringify( rules ) );

		if ( !Array.isArray( rules ) || rules.length === 0 ) {
			console.warn( '[QualifierConfirmation] No rules configured, aborting.' );
			return;
		}

		/**
		 * Extract a plain string value from a Wikibase datavalue object.
		 * Handles string, monolingualtext, and quantity types.
		 *
		 * @param {Object|string} datavalue
		 * @return {string}
		 */
		function extractValue( datavalue ) {
			if ( typeof datavalue === 'string' ) {
				return datavalue;
			}
			if ( datavalue && typeof datavalue === 'object' ) {
				var v = datavalue.value;
				if ( typeof v === 'string' ) {
					return v;
				}
				if ( v && typeof v === 'object' ) {
					// monolingualtext
					if ( typeof v.text === 'string' ) {
						return v.text;
					}
					// quantity
					if ( typeof v.amount === 'string' ) {
						return v.amount;
					}
					// wikibase-entityid (Item / Property)
					if ( typeof v.id === 'string' ) {
						return v.id;
					}
					// time
					if ( typeof v.time === 'string' ) {
						return v.time;
					}
					// globe-coordinate
					if ( typeof v.latitude === 'number' && typeof v.longitude === 'number' ) {
						return v.latitude + ',' + v.longitude;
					}
				}
			}
			return String( datavalue );
		}

		/**
		 * Given a parsed claim object (from the `claim` wbsetclaim parameter),
		 * return the first matching rule or null.
		 *
		 * @param {Object} claim
		 * @return {Object|null}
		 */
		function findMatchingRule( claim ) {
			var qualifiers = claim.qualifiers;
			if ( !qualifiers || typeof qualifiers !== 'object' ) {
				return null;
			}

			for ( var i = 0; i < rules.length; i++ ) {
				var rule = rules[ i ];
				var snaks = qualifiers[ rule.qualifierProperty ];

				if ( !Array.isArray( snaks ) ) {
					continue;
				}

				for ( var j = 0; j < snaks.length; j++ ) {
					var snak = snaks[ j ];
					if ( snak.snaktype !== 'value' ) {
						continue;
					}
					if ( !snak.datavalue ) {
						continue;
					}
					var value = extractValue( snak.datavalue );
					if ( value.toLowerCase() === rule.qualifierValue.toLowerCase() ) {
						return rule;
					}
				}
			}

			return null;
		}

		// Patch mw.Api.prototype.post to intercept wbsetclaim calls.
		var originalPost = mw.Api.prototype.post;
		console.log( '[QualifierConfirmation] Patching mw.Api.prototype.post' );

		mw.Api.prototype.post = function ( params, options ) {
			var self = this;
			var args = arguments;

			console.log( '[QualifierConfirmation] mw.Api.post called, action:', params && params.action );

			// Only intercept wbsetclaim
			if ( !params || params.action !== 'wbsetclaim' ) {
				return originalPost.apply( self, args );
			}

			var claimRaw = params.claim;
			var claim;
			try {
				claim = typeof claimRaw === 'string' ? JSON.parse( claimRaw ) : claimRaw;
			} catch ( e ) {
				return originalPost.apply( self, args );
			}

			if ( !claim ) {
				return originalPost.apply( self, args );
			}

			console.log( '[QualifierConfirmation] wbsetclaim intercepted. Claim qualifiers:', JSON.stringify( claim.qualifiers ) );

			var rule = findMatchingRule( claim );
			console.log( '[QualifierConfirmation] Matching rule:', rule ? JSON.stringify( rule ) : 'none' );
			if ( !rule ) {
				return originalPost.apply( self, args );
			}

			// Return a jQuery Deferred that resolves/rejects after user interaction.
			var deferred = $.Deferred();

			OO.ui.confirm( rule.confirmationMessage, {
				title: mw.msg( 'qualifierconfirmation-dialog-title' )
			} ).done( function ( confirmed ) {
				if ( confirmed ) {
					originalPost.apply( self, args )
						.then(
							function () { deferred.resolve.apply( deferred, arguments ); },
							function () { deferred.reject.apply( deferred, arguments ); }
						);
				} else {
					// Reject with an object that Wikibase recognises as a user-initiated cancel
					// (empty string avoids an additional error toast in the UI).
					deferred.reject( 'qualifierconfirmation-cancelled', {} );
				}
			} );

			return deferred.promise();
		};
	} );

}() );
