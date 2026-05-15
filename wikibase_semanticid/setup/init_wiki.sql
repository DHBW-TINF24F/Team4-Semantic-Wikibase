-- Seed script for Wiki initialization
-- Target: Main Page content + optional CirrusSearch frozen index fix

START TRANSACTION;

-- Keep Main Page title canonical
UPDATE page
SET page_title = 'Main_Page'
WHERE page_id = 1;

-- HTML payload for homepage (kept in SQL for reproducible DB bootstrap)
SET @homepage_html = '<div class="semanticid-homepage" style="max-width:980px;margin:2rem auto;padding:1.5rem;font-family:Arial,Helvetica,sans-serif;line-height:1.6;"><h1 style="margin-top:0;">Willkommen im Semantic Wikibase</h1><p>Diese Wikibase-Instanz dient als zentrale Wissensbasis für semantische Begriffe, Eigenschaften und Referenzen.</p><h2>Schnellstart</h2><ol><li>Lege eine Property für die Semantic ID an (standardmäßig <strong>P1</strong>).</li><li>Erstelle ein Item und ergänze die Semantic ID als Statement.</li><li>Öffne das Item direkt über den Semantic-ID-Pfad.</li></ol><h2>Hinweise</h2><ul><li>Die Suche wird beim Initialisieren automatisch neu indexiert.</li><li>Die Startseite wird bei der Entwicklungsinitialisierung automatisch gesetzt.</li></ul></div>';

SET @target_page_id = 1;
SET @old_rev_id = (SELECT page_latest FROM page WHERE page_id = @target_page_id);
SET @actor_id = COALESCE((SELECT rev_actor FROM revision WHERE rev_id = @old_rev_id), 1);
SET @comment_id = COALESCE((SELECT rev_comment_id FROM revision WHERE rev_id = @old_rev_id), 1);
SET @rev_timestamp = DATE_FORMAT(UTC_TIMESTAMP(), '%Y%m%d%H%i%s');

INSERT INTO text (old_text, old_flags)
VALUES (@homepage_html, 'utf-8');
SET @text_id = LAST_INSERT_ID();

INSERT INTO content (content_size, content_sha1, content_model, content_format, content_address)
VALUES (
  CHAR_LENGTH(@homepage_html),
  SHA1(@homepage_html),
  'wikitext',
  'text/x-wiki',
  CONCAT('tt:', @text_id)
);
SET @content_id = LAST_INSERT_ID();

INSERT INTO revision (
  rev_page,
  rev_comment_id,
  rev_actor,
  rev_timestamp,
  rev_minor_edit,
  rev_deleted,
  rev_len,
  rev_parent_id,
  rev_sha1,
  rev_content_model,
  rev_content_format
) VALUES (
  @target_page_id,
  @comment_id,
  @actor_id,
  @rev_timestamp,
  0,
  0,
  CHAR_LENGTH(@homepage_html),
  @old_rev_id,
  SHA1(@homepage_html),
  'wikitext',
  'text/x-wiki'
);
SET @new_rev_id = LAST_INSERT_ID();

INSERT INTO slots (
  slot_revision_id,
  slot_role_id,
  slot_content_id,
  slot_origin,
  slot_sha1
) VALUES (
  @new_rev_id,
  1,
  @content_id,
  @new_rev_id,
  SHA1(@homepage_html)
);

UPDATE page
SET
  page_latest = @new_rev_id,
  page_touched = @rev_timestamp,
  page_len = CHAR_LENGTH(@homepage_html)
WHERE page_id = @target_page_id;

-- Optional: set CirrusSearch frozen index marker (manual fix replacement)
INSERT INTO updatelog (ul_key, ul_value)
VALUES ('cirrussearch_frozen_index', '1')
ON DUPLICATE KEY UPDATE ul_value = VALUES(ul_value);

COMMIT;
