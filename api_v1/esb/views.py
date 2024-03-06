from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse

from . import RabbitMQManager
from .schemas import Package, PackageMessage, GetMessages, Ask


router = APIRouter(tags=["esb"])

rabbitmq_manager = RabbitMQManager()


@router.get("/initialize", status_code=status.HTTP_200_OK)
def initialize_queues():
    """
    # Инициализация очередей
    ```BSL
        Заголовки = Новый Соответствие;
        Заголовки.Вставить("content-type", "application/json");

        HTTPЗапрос = Новый HTTPЗапрос("/api/v1/initialize", Заголовки);
        HTTPСоединение = Новый HTTPСоединение("localhost", 80);
        Ответ = HTTPСоединение.ВызватьHTTPМетод("GET", HTTPЗапрос);
        СодержимоеОтвета = Ответ.ПолучитьТелоКакСтроку();
        Если Не Ответ.КодСостояния = 200 Тогда
            Сообщить("Ответ сервера: '" + СодержимоеОтвета + "', затрачено: " + Строка(ТекущаяДата()-Старт) + ", код ответа: " + Ответ.КодСостояния);
            Возврат;
        КонецЕсли;
    ```
    """
    rabbitmq_manager.initialize_queues()
    return JSONResponse(
        content={"message": "Очереди инициализированы"}, status_code=status.HTTP_200_OK
    )


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
