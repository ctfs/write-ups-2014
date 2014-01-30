#!/bin/sh

set -e

# Add or modify any build steps you need here
cd "$(dirname "$0")"
sbt="dependencies/sbt"

if [ ! -f "$sbt" ]; then
  echo "It looks like you deleted the sbt dependency from dependencies/. You'll need it for the rest of this project."
  exit 1
fi

"$sbt" assembly

