INSERT INTO challenge.trusted.events (
    event_id,
    timestamp,
    event_type,
    user_id,
    document_id,
    comment_text,
    edit_length,
    shared_with,
    _source_file,
    _ingested_at,
	day_of_week
)
SELECT
    re.event_id,
    re.timestamp,
    re.event_type,
    re.user_id,
    re.document_id,
    re.comment_text,
    CAST(NULLIF(re.edit_length,'') AS INT) AS edit_length,
    re.shared_with,
    re._source_file,
    re._ingested_at,
	To_Char(re.timestamp, 'Day') day_of_week
FROM challenge.raw.events re
ON CONFLICT (event_id) DO UPDATE SET
    timestamp = EXCLUDED.timestamp,
    event_type = EXCLUDED.event_type,
    user_id = EXCLUDED.user_id,
    document_id = EXCLUDED.document_id,
    comment_text = EXCLUDED.comment_text,
    edit_length = EXCLUDED.edit_length,
    shared_with = EXCLUDED.shared_with,
    _source_file = EXCLUDED._source_file,
    _ingested_at = EXCLUDED._ingested_at;
