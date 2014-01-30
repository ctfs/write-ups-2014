#!/bin/sh
#
# Usage: ./build.sh [-q]
#
# -q: Don't print sqlcluster usage after the build. (Defaults to true
#     if stdout is not a TTY.)

set -e

cd "$(dirname "$0")"
cwd=$(pwd -P)

if ! type sqlite3 >/dev/null 2>/dev/null; then
    echo "You don't have a \`sqlite3\` command in your PATH!"
    echo
    echo "You need to have a working sqlite3 in order to run"
    echo "sqlcluster. (HINT: all you should have to do is install"
    echo "the sqlite3 package through your package manager.)"
    exit 1
fi

# By default, install dependencies locally (to the .build tree), so
# out-of-date dependencies don't cause weird build issues.
#
# On our build boxes, we'll set this variable to true so you don't
# need to fetch all the dependencies yourself. You can set
# CTF_BUILD_ENV if you'd like to do this locally.
if [ -z "${CTF_BUILD_ENV}" ]; then
    export GOPATH="$cwd/.build"
else
    export GOPATH="$cwd/.build:$GOPATH"
fi

echo "Fetching sqlcluster dependencies..."
go get -d

echo "Building sqlcluster binary..."
go build -o sqlcluster

if [ ! -t 1 ] || [ "$1" = "-q" ]; then
    echo "Successfully built sqlcluster."
else
    echo "Successfully built sqlcluster. Run directly, or under \`test/harness\`."
    echo
    echo "/"
    ( "$cwd/sqlcluster" -h 2>&1 | sed 's/^/|  /' ) || true
    echo "\\"
fi
