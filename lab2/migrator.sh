#!/bin/bash

cd "scripts"

export PGPASSWORD='postgres'

function run_sql() {
  /c/Program\ Files/PostgreSQL/16/bin/psql.exe -U postgres -d lab2_mo_rpp -f "$1"
}

function run_sql_c() {
  /c/Program\ Files/PostgreSQL/16/bin/psql.exe -U postgres -d lab2_mo_rpp -t -c "$1"
}

run_sql_c "CREATE TABLE IF NOT EXISTS migrations (id SERIAL PRIMARY KEY, migration_name VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"

function run_migration() {
  applied_migrations=$(run_sql_c "SELECT migration_name FROM migrations;")
  echo "============================"
  echo "Migrations that have already been applied:"
  echo "$applied_migrations"
  echo "============================"
  files=$(find -maxdepth 1 -type f)
  echo "The beginning of migration..."

  for file in $files; do
    matched=false
    if echo ${applied_migrations[@]} | grep -q -w "$file"; then 
      matched=true;
    fi
    if [ $matched == false ]; then
        run_sql_c "INSERT INTO migrations(migration_name) VALUES ('$file');";
        run_sql $file
        echo "Applied! Script $file is successfully completed.";
      else
        echo "Skipped. Script $file is already applied.";
    fi
  done
  echo "Data migration is completed."
}

"$@"

run_migration