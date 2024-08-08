# mcs_esb
Шина данных для RabbitMQ
## Описание
Проект представляет собой шину данных и реализует взаимодействие с RabbitMQ через API.
Проект состоит из 2-х сервисов:
1. API - сервис для взаимодействия с RabbitMQ
2. RabbitMQ - брокер сообщений

## Установка
1. Установить [Docker](https://www.docker.com/products/docker-desktop)
2. Установить [Docker Compose](https://docs.docker.com/compose/install/)
3. Склонировать репозиторий
> git clone https://github.com/ipyguru/mcs_esb.git
4. Перейти в папку с проектом
5. Выполнить команду `docker-compose up -d`
6. Перейти по адресу `http://localhost:15672/` и войти в RabbitMQ с логином `guest` и паролем `guest`
7. Можно использовать

## Использование
1. Перейти в api по адресу `http://localhost/docs`
2. Использовать методы для отправки и получения сообщений
3. Перейти в RabbitMQ по адресу `http://localhost:15672/` и посмотреть сообщения в очередях
4. При необходимости можно посмотреть логи сервисов командой `docker-compose logs -f`
5. При необходимости можно остановить сервисы командой `docker-compose down`
6. При необходимости можно удалить сервисы командой `docker-compose down -v`
7. При необходимости можно удалить образы командой `docker rmi $(docker images -q)`
8. При необходимости можно удалить вольюмы командой `docker volume prune`
9. При необходимости можно удалить сети командой `docker network prune`
10. При необходимости можно удалить контейнеры командой `docker rm $(docker ps -a -q)`
11. При необходимости можно удалить все командой `docker system prune -a`

## Обновление из репозитория
1. Перейти в папку с проектом
2. Получить изменения из репозитория командой `git pull`
3. Перезапустить сервисы командой `docker-compose up -d --no-deps --build`

## Если не срабатывает git push
1. Перейти в папку с проектом
2. Выполнить команду `eval "$(ssh-agent -s)"` для запуска ssh-agent
3. Выполнить команду `--apple-use-keychain ~/.ssh/id_ed25519` для добавления ключа в ssh-agent
4. Выполнить команду `ssh-add -K ~/.ssh/id_ed25519` для добавления ключа в ssh-agent
5. Попробовать выполнить команду `git push`

## Авторы
- [vbuoc](vbuoc@yandex.ru), [github](https://github.com/ipyguru)

## Лицензия
Этот проект лицензирован по лицензии MIT - подробности см. в файле [LICENSE](LICENSE)

## Дополнительно
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

