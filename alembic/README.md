# Работа с миграциями
## Перед применением миграций
```python
1. В core.__init__.py убедиться, что в переменной __all__ прописаны все модели 
```

## Сгенерировать миграцию
```python
alembic revision --autogenerate -m "name_of_migration" 
```
## Обновиться до последней миграции
```python
alembic upgrade head
```
## Откатиться на одну миграцию назад
```python
alembic downgrade -1
```
## Откатиться на несколько миграций назад
```python
alembic downgrade -2
```
## Откатиться до начального состояния
```python
alembic downgrade base
```
## Показать текущую миграцию
```python
alembic current
```
## Показать все миграции
```python
alembic history
```
## Показать все миграции в виде SQL
```python
alembic history --sql
```