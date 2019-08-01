#!/bin/bash

BASENAME="$(readlink -f "$0")"
BASEDIR="$(dirname "$BASENAME")"
BASENAME="$(basename "$BASENAME")"

PYTHON=$HOME/.venv/bin/python3

[[ -x "$PYTHON" ]] || PYTHON=python3


log () {
	printf "%s\n" "$*" >&2
}

err() {
	log "$*"
	exit 2
}

help() {
	err usage: "$BASENAME" capturename
}

analysis() {
	local name="$1"

	[[ -e "$name" ]] && name="$(realpath "$name")"

	local bname="$(basename "$name")"

	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -f "$BASEDIR/sql/latency-hist.sql" > "${bname}.hist.csv"
	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -f "$BASEDIR/sql/dump-worst.sql" > "${bname}.worst.csv"
	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -f "$BASEDIR/sql/dump-worst-filtered.sql" > "${bname}.worst-filtered.csv"
	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -f "$BASEDIR/sql/dump-percentiles.sql" > "${bname}.percentiles.csv"
	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -f "$BASEDIR/sql/dump-percentiles-filtered.sql" > "${bname}.percentiles-filtered.csv"
	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -f "$BASEDIR/sql/dump-transferrate.sql" > "${bname}.transferrate.csv"

	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -v "type=pre" -f "$BASEDIR/sql/jitter-hist.sql" > "${bname}.jitterpre.csv"
	psql -q -X -v ON_ERROR_STOP=1 -v "name=$name" -v "type=post" -f "$BASEDIR/sql/jitter-hist.sql" > "${bname}.jitterpost.csv"
}

test $# -lt 1 && help

analysis "$@"
