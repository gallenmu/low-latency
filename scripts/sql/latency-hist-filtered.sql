\set bucket 100

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
		AND ts > (1000000000 + (SELECT MIN(ts) from pkt))
)

SELECT *, count(*) FROM (
    SELECT mpcaps.latency_bucket
    FROM (
	SELECT
		pre.ts AS prets,
		post.ts as postts,
            ((post.ts - pre.ts) / :bucket ) * :bucket AS latency_bucket
        FROM  pre JOIN  post USING (hdr) 
        WHERE post.ts > pre.ts 
            AND post.ts < pre.ts + 5 * 1e9   
        ORDER BY pre.ts ASC
    ) AS mpcaps
) AS histogram
GROUP BY histogram.latency_bucket
ORDER BY histogram.latency_bucket ASC
;

\copy (select * from export order by latency_bucket) to pstdout csv header
