по адресу http://127.0.0.1:8000/upload/file/ отправляем файл bills.xlsx или client_org.xlsx

key - file, value - файл

первым client_org.xlsx, затем bills.xlsx

Данные записываются в таблицы БД Client, Organization и Bill

Эндпоинт со списком счетов с возможностью фильтровать по организации, клиенту http://127.0.0.1:8000/api/v1/bills
Принимает:  client          - название клиента, текстом
            organization    - название организации, текстом

Эндпоинт клиентов http://127.0.0.1:8000/api/v1/client - не успел реализовать рассчет