create temp view export as

WITH

pre AS (

	select ts, hdr from (
		SELECT ts, hdr, count(1) over (partition by hdr) as c
		FROM pkt
		JOIN capture USING (capture_id)
		WHERE
			capture.name = :'name'
			AND capture."type" = 'pre'
	) as yolo where c = 1
)

, post AS (
	SELECT ts, hdr
	FROM pkt
	JOIN capture USING (capture_id)
	WHERE
		capture.name = :'name'
		AND capture."type" = 'post'
)

SELECT
	post.ts - pre.ts as latency,
	pre.ts AS prets,
	post.ts as postts,
	encode(pre.hdr, 'hex')
FROM  pre JOIN  post USING (hdr)
WHERE post.ts > pre.ts
    AND post.ts < pre.ts + 5 * 1e9
;

\copy (select percentile_disc(0.5) within group (order by latency) as perc_50, percentile_disc(0.9) within group (order by latency) as perc_90, percentile_disc(0.99) within group (order by latency) as perc_99, percentile_disc(0.999) within group (order by latency) as perc_999, percentile_disc(0.9999) within group (order by latency) as perc_9999, percentile_disc(0.99999) within group (order by latency) as perc_99999, percentile_disc(0.999999) within group (order by latency) as perc_999999, max(latency) as maximum from export) to pstdout csv header
