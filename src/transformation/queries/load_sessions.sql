INSERT INTO challenge.marts.sessions (
with events as(
SELECT
	event_id
	, user_id
	, timestamp
	, lead(timestamp,1) over (partition by user_id order by timestamp) next_interaction
FROM CHALLENGE.trusted.events
)

, diff AS(
select
	event_id
	, user_id
	, timestamp
	, next_interaction
	, extract(epoch from(next_interaction - timestamp)) / 60 minutes_transcurred
from events
)

select
	event_id
	, user_id
	, timestamp
	, next_interaction
	, minutes_transcurred
	, least(minutes_transcurred, 30) session_duration --Llamamos sesion a la diferencia entre eventos, con tiempo maximo 30 minutos
from diff
order by minutes_transcurred
)
