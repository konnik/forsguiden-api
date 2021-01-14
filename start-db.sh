#!/bin/bash

# Lägg till denna rad i din .env 
# DATABASE_URL=postgres://postgres:password@localhost/postgres

docker run -it --rm \
   --name forsguiden-postgres \
   -e POSTGRES_PASSWORD=password \
   -p 5432:5432 \
   postgres
