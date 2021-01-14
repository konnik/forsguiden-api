#!/bin/bash

set -e

if [ -d ./flyway-7.5.0/ ]; then
    echo "Använder befintlig flyway."
else
    echo "Laddar ned och packar upp flyway..."
    wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/7.5.0/flyway-commandline-7.5.0-linux-x64.tar.gz | tar xz
fi

if [ -f .env ]; then
    echo "Läser JDBC_DATABASE_URL från .env"
    source .env
fi

export FLYWAY_URL=$JDBC_DATABASE_URL

echo "Kör flyway med $FLYWAY_URL"
./flyway-7.5.0/flyway migrate -n

