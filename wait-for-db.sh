#!/bin/bash

# Ждем пока PostgreSQL будет готов
echo "⏳ Waiting for PostgreSQL to be ready..."

until PGPASSWORD=blog_password psql -h "postgres" -U "blog_user" -d "blog_db" -c '\q'; do
  echo "📊 PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is ready!"