#!/bin/sh

# Ждем, пока база данных станет доступной
echo "Ждем, пока база данных будет доступна..."
while ! nc -z db 5432; do
  sleep 1
  echo "..."
done
echo "База данных доступна"

# Выполняем миграции
echo "Выполняем миграции Alembic..."
alembic upgrade head

# Запускаем приложение
echo "Запускаем приложение..."
exec "$@"
