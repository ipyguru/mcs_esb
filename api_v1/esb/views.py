from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse

from . import RabbitMQManager
from .schemas import Package, PackageMessage, GetMessages, Ask, Exchange, Queue, Bind


router = APIRouter(tags=["esb"])

rabbitmq_manager = RabbitMQManager()


@router.post("/publish", response_model=Package, status_code=status.HTTP_201_CREATED)
def publish_messages(package: Package):
    """
    # Отправка пакета сообщения в очередь
    ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/publish", Заголовки);
        ПараметрыПреобразования = Новый Структура("ПереносСтрок", ПереносСтрокJSON.Нет);
        HTTPЗапрос.УстановитьТелоИзСтроки(КоннекторHTTP.ОбъектВJson(Сообщение, ПараметрыПреобразования),"UTF-8", ИспользованиеByteOrderMark.НеИспользовать);

        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("POST", HTTPЗапрос);

        Возврат Ответ.КодСостояния;
    ```
    """
    for message in package.package_messages.messages:
        try:
            rabbitmq_manager.publish_message(package, message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            ) from e

    return package


@router.post("/get", response_model=PackageMessage, status_code=status.HTTP_200_OK)
def get_messages(query: GetMessages):
    """
    # Получение пакета сообщений из очереди
     ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/get", Заголовки);

        Сообщение = Новый Структура("exchange, queue", "amq.topic", "catalog");
        ПараметрыПреобразования = Новый Структура("ПереносСтрок", ПереносСтрокJSON.Нет);
        HTTPЗапрос.УстановитьТелоИзСтроки(
            КоннекторHTTP.ОбъектВJson(Сообщение, ПараметрыПреобразования),"UTF-8", ИспользованиеByteOrderMark.НеИспользовать
        );

        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("POST", HTTPЗапрос);
        СодержимоеОтвета = Ответ.ПолучитьТелоКакСтроку();
        Если Не Ответ.КодСостояния = 200 Тогда
            Сообщить("Ответ сервера: '" + СодержимоеОтвета + "', затрачено: " + Строка(ТекущаяДата()-Старт) + ", код ответа: " + Ответ.КодСостояния);
            Возврат;
        КонецЕсли;

        ПакетСообщений = Десериализовать(СодержимоеОтвета);
        Для каждого Сообщение Из ПакетСообщений.Сообщения Цикл
            ...
        КонецЦикла;
    ```
    """
    package_message = rabbitmq_manager.get_messages(query)
    return package_message


@router.post("/ask", status_code=status.HTTP_200_OK)
def ask_messages(query: Ask):
    """
    # Подтверждение получения сообщений из очереди
    ```BSL
        ЗагрузкаПодтверждена = ПодтвердитьЗагрузкуСообщений(Новый Структура("delivery_tags",УспешноЗагруженные));
        ...
        Функция ПодтвердитьЗагрузкуСообщений(СтруктураУспешноЗагруженных)
            Заголовки = Новый Соответствие;
            Заголовки.Вставить("content-type", "application/json");

            HTTPЗапрос = Новый HTTPЗапрос("/api/v1/ask", Заголовки);
            ПараметрыПреобразования = Новый Структура("ПереносСтрок", ПереносСтрокJSON.Нет);
            HTTPЗапрос.УстановитьТелоИзСтроки(
                КоннекторHTTP.ОбъектВJson(СтруктураУспешноЗагруженных, ПараметрыПреобразования),"UTF-8", ИспользованиеByteOrderMark.НеИспользовать
            );

            HTTPСоединение = Новый HTTPСоединение("localhost", 80);
            Ответ = HTTPСоединение.ВызватьHTTPМетод("POST", HTTPЗапрос);

            //
            СтруктураОтвета.Содержание = "" + Десериализовать(Ответ.ПолучитьТелоКакСтроку()).message;
            СтруктураОтвета.Успех = Ответ.КодСостояния = 200;
            Возврат СтруктураОтвета;
        КонецФункции;
    ```
    """

    response = rabbitmq_manager.ask_messages(query)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@router.post("/exchange_declare", status_code=status.HTTP_200_OK)
def exchange_declare(exchange: Exchange):
    """
    # Объявление обменника
    ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/exchange_declare", Заголовки);
        ПараметрыПреобразования = Новый Структура("ПереносСтрок", ПереносСтрокJSON.Нет);
        HTTPЗапрос.УстановитьТелоИзСтроки(КоннекторHTTP.ОбъектВJson(Объявление, ПараметрыПреобразования),"UTF-8", ИспользованиеByteOrderMark.НеИспользовать);

        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("POST", HTTPЗапрос);

        Возврат Ответ.КодСостояния;
    ```
    """
    rabbitmq_manager.exchange_declare(exchange)
    return JSONResponse(
        content={"message": "Объявление обменника прошло успешно"},
        status_code=status.HTTP_200_OK,
    )


@router.post("/queue_declare", status_code=status.HTTP_200_OK)
def queue_declare(queue: Queue):
    """
    # Объявление очереди
    ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/queue_declare", Заголовки);
        ПараметрыПреобразования = Новый Структура("ПереносСтрок", ПереносСтрокJSON.Нет);
        HTTPЗапрос.УстановитьТелоИзСтроки(КоннекторHTTP.ОбъектВJson(Объявление, ПараметрыПреобразования),"UTF-8", ИспользованиеByteOrderMark.НеИспользовать);

        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("POST", HTTPЗапрос);

        Возврат Ответ.КодСостояния;
    ```
    """
    rabbitmq_manager.queue_declare(queue)
    return JSONResponse(
        content={"message": "Объявление очереди прошло успешно"},
        status_code=status.HTTP_200_OK,
    )


@router.post("/bind", status_code=status.HTTP_200_OK)
def queue_bind(bind: Bind):
    """
    # Привязка очереди к обменнику
    ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/bind", Заголовки);
        ПараметрыПреобразования = Новый Структура("ПереносСтрок", ПереносСтрокJSON.Нет);
        HTTPЗапрос.УстановитьТелоИзСтроки(КоннекторHTTP.ОбъектВJson(Привязка, ПараметрыПреобразования),"UTF-8", ИспользованиеByteOrderMark.НеИспользовать);

        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("POST", HTTPЗапрос);

        Возврат Ответ.КодСостояния;
    ```
    """
    rabbitmq_manager.queue_bind(bind)
    return JSONResponse(
        content={"message": "Привязка очереди к обменнику прошла успешно"},
        status_code=status.HTTP_200_OK,
    )


@router.get("/connectionClose", status_code=status.HTTP_200_OK)
def connection_close():
    """
    # Закрытие соединения
    ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/connectionClose", Заголовки);
        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("GET", HTTPЗапрос);
        СодержимоеОтвета = Ответ.ПолучитьТелоКакСтроку();
        Если Не Ответ.КодСостояния = 200 Тогда
            Сообщить("Ответ сервера: '" + СодержимоеОтвета + "', затрачено: " + Строка(ТекущаяДата()-Старт) + ", код ответа: " + Ответ.КодСостояния);
            Возврат;
        КонецЕсли;
    ```
    """
    rabbitmq_manager.close()
    return JSONResponse(
        content={"message": "Соединение закрыто"}, status_code=status.HTTP_200_OK
    )