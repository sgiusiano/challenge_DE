INSERT INTO challenge.trusted.documents(
document_id
, created_at
, last_modified
, document_word_count
, comment_count
, shared_with_count
)
SELECT
	document_id
	, min(timestamp) created_at
	, max(timestamp) last_modified
	, sum(cast(nullif(edit_length, '') as int)) document_word_count
    , count(distinct case when event_type='comment_added' then event_id else null end) - 1 comment_count
	, count(distinct case when event_type='document_shared' then shared_with else null end) - 1 shared_with_count
FROM challenge.raw.events
WHERE event_type in ('document_edit', 'comment_added', 'document_shared')
GROUP BY 1
ON CONFLICT (document_id) DO UPDATE SET
document_word_count=EXCLUDED.document_word_count,
comment_count=EXCLUDED.comment_count,
last_modified=EXCLUDED.last_modified,
shared_with_count=EXCLUDED.shared_with_count;
