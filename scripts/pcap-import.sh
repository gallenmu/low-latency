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
	err usage: "$BASENAME" /path/to/capture-pre.pcap [capturename]
}

import() {
	local prepcap="$1"
	local name="$2"

	[[ "$prepcap" == *-pre-*.pcap ]] || err input \""$prepcap"\" does not match expected pattern

	test -r "$prepcap" || err can not read pre cap: \""$prepcap"\"

	test -n "$name" || name="$(realpath "${prepcap}")"

	local postpcap="${prepcap/-pre-/-post-}"

	test -r "$postpcap" || err can not read post cap: \""$postpcap"\"

	( "$PYTHON" "${BASEDIR}/pcap-to-csv.py" "$prepcap" | psql -X -v ON_ERROR_STOP=1 --pset pager=off -v "name=${name}" -v type=pre -f "${BASEDIR}/sql/load.sql" ) &
	local prej=$!
	( "$PYTHON" "${BASEDIR}/pcap-to-csv.py" "$postpcap" | psql -X -v ON_ERROR_STOP=1 --pset pager=off -v "name=${name}" -v type=post -f "${BASEDIR}/sql/load.sql" ) &
	local postj=$!

	log $prej
	log $postj

	wait $prej || { log import of \""$prepcap"\" failed. ; error=true; }
	wait $postj || { log import of \""$postpcap"\" failed. ; error=true; }

	[[ -n "$error" ]] && err failed to import
}

setupdb(){
	su postgres -c "createuser -s root" || true
	createdb root
	psql -1 -X -v ON_ERROR_STOP=1 --pset pager=off -f "${BASEDIR}/sql/ddl.sql"
}


test $# -lt 1 && help

setupdb

import "$@"
