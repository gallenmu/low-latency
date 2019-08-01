create temp view export as

WITH

pre AS (

	SELECT ts, hdr
	FROM pkt
	JOIN capture USING (capture_id)
	WHERE
		capture.name = :'name'
		AND capture."type" = 'pre'

),
post AS (
	SELECT ts, hdr
	FROM pkt
	JOIN capture USING (capture_id)
	WHERE
		capture.name = :'name'
		AND capture."type" = 'post'
),
postcount AS (
	SELECT COUNT(*) AS countpost
	FROM post
),
precount AS (
	SELECT COUNT(*) AS countpre
	FROM pre
)

SELECT
	*,
	CAST(countpost as decimal)/countpre as transferrate
FROM precount, postcount
;

\copy (select * from export) to pstdout csv header
