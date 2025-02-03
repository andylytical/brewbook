#!/usr/bin/bash

set -x

OUTFILE=/var/lib/postgresql/data/"$(date +%Y%m%dT%H%M%S%z)".sql
pg_dump \
  -h localhost \
  -p 5432 \
  -U $POSTGRES_USER \
  -d $POSTGRES_DB \
  -a \
  -t 'public.inventory_*' \
  -f ${OUTFILE}
