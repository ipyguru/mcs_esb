# mcs_esb
Шина данных для ЛегПромРазвития

# Работа с миграциями
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

