#!/bin/bash

# Ждем пока PostgreSQL будет готов
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! pg_isready -h postgres -p 5432 -U blog_user -d blog_db; do
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Применяем миграции
echo "🗃️ Applying database migrations..."
alembic upgrade head

echo "🎉 Database initialization complete!"