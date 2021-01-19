#!/bin/bash

set -e

if [ -f .env ]; then
    echo "Läser JDBC_DATABASE_URL från .env"
    source .env
fi

if [[ -z "$JDBC_DATABASE_URL" ]]; then
   echo "JDBC_DATABASE_URL måste sättas"
   exit 1
fi

#export FLYWAY_URL=$JDBC_DATABASE_URL

./mvnw flyway:clean -Dflyway.locations=filesystem:sql -Dflyway.url=$JDBC_DATABASE_URL
