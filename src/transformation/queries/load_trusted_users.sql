INSERT INTO challenge.trusted.users (
user_id
, username
, last_seen
, days_from_last_activity
, created_at
)
SELECT
	user_id
	, concat('username_', user_id) username
	, max(timestamp) as last_seen
	, current_date - cast(max(timestamp) as date) as days_from_last_activity
	, min(timestamp) created_at
FROM challenge.raw.events
GROUP BY 1
ON CONFLICT (user_id) DO UPDATE SET
    last_seen = EXCLUDED.last_seen,
    days_from_last_activity = EXCLUDED.days_from_last_activity;
