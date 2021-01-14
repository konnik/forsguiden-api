#!/bin/bash

set -e

if [ -f .env ]; then
    echo "Läser JDBC_DATABASE_URL från .env"
    source .env
fi

export FLYWAY_URL=$JDBC_DATABASE_URL

echo "Kör flyway med $FLYWAY_URL"
mvn flyway:migrate -Dflyway.locations=filesystem:sql
