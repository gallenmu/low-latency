\set bucket 100

create temp view export as

WITH pkts AS (
	SELECT ts, hdr
	FROM pkt
	JOIN capture USING (capture_id)
	WHERE
		capture.name = :'name'
		AND capture."type" = :'type'
)

select bucket, count(1)
from (
	select ((ts - lag(ts) over (order by ts))/:bucket)*:bucket as bucket
	from pkts
	) as jitter
where bucket is not null
group by bucket
order by bucket asc
;

\copy (select * from export order by bucket) to pstdout csv header
;
