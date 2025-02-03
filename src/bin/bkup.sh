#!/usr/bin/bash

set -x

BASE="${HOME}"/working/personal/brewbook
BIN="${BASE}"/src/bin
PG_DIR="${BASE}"/src/data/db
BKUP_DIR="${BASE}"/backups
TS=$( date +%Y%m%dT%H%M%S )


install_dump_script() {
  set -x
  # copy bash script into place 
  sudo install -t "${PG_DIR}" -o root -g root -m '0700' "${BIN}"/mk_sql_dump.sh
}


sync_backup_files() {
  set -x
  sudo find "${PG_DIR}" -type f -name '*.sql' -print \
  | xargs -r sudo install -o aloftus -g aloftus -m '0660' -t "${BKUP_DIR}"
}


sync_restore_sources() {
  set -x
  find "${BKUP_DIR}" -type f -name '*.sql' -print \
  | xargs -r sudo install -o 999 -g 0 -m '0600' -t "${PG_DIR}"
}


###
# MAIN
###

ENDWHILE=0
while [[ $# -gt 0 ]] && [[ $ENDWHILE -eq 0 ]] ; do
  case $1 in
    install)
      install_dump_script;;
    copy|save)
      sync_backup_files;;
    push|restore)
      sync_restore_sources;;
    --) ENDWHILE=1;;
    *) echo "Invalid action '$1'"; exit 1;;
  esac
  shift
done
