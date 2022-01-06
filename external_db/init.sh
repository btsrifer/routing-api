psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'routing'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE routing"

psql -U postgres -d routing -a -f opt/schema_queries/create_schema.sql

psql -U postgres -d routing -a -f opt/schema_queries/insert.sql
