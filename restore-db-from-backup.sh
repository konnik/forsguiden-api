#!/bin/bash

set -e

export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=password

pg_restore --clean --verbose --no-acl --no-owner --dbname postgres ./db-backup/latest.dump 




