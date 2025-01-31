#!/usr/bin/bash

set -x

PG_DIR="${HOME}"/working/personal/brewbook/src/data/db
BKUP_DIR="${HOME}"/working/personal/brewbook/backups
TS=$( date +%Y%m%dT%H%M%S )


sync_restore_sources() {
  set -x
  find "${BKUP_DIR}" -type f -name '*.sql' -print \
  | xargs -r sudo install -o 999 -g 0 -m '0600' -t "${PG_DIR}"
}


sync_backup_files() {
  set -x
  sudo find "${PG_DIR}" -type f -name '*.sql' -print \
  | xargs -r sudo install -o aloftus -g aloftus -m '0660' -t "${BKUP_DIR}"
}


sync_restore_sources

sync_backup_files
