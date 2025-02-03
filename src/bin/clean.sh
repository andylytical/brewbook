#!/usr/bin/bash

set +x

DELETE=(
  $( sudo find src -type d -name data )
  $( find src -type d -name migrations )
)

for dir in "${DELETE[@]}"; do
  sudo rm -rf "${dir}"
done
