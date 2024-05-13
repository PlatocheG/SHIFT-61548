# SHIFT-61548 - Тестовое задание на курс «Python»



## Описание задачи:

Реализуйте REST-сервис просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности, вам
потребуется реализовать метод где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.

## Требования к решению:

Обязательные технические требования:
- код размещен и доступен в публичном репозитории на GitLab;
- оформлена инструкция по запуску сервиса и взаимодействию с проектом (Markdown файл с использованием конструкций разметки от GitLab по необходимости);
- сервис реализован на FastAPI.

Необязательные технические требования (по возрастанию трудоемкости):
- зависимости зафиксированы менеджером зависимостей poetry;
- написаны тесты с использованием pytest;
- реализована возможность собирать и запускать контейнер с сервисом в Docker.

Вы можете выполнить только часть необязательных технических требований.
Задание будет оцениваться комплексно.


## Реализация:

- Хранение данных       - SQLite;
- Работа с БД           - SQLAlchemy (core);
- Хэширование паролей   - библиотека bcrypt;
- Токен валидации       - библиотека pyjwt;

Реализованы три URL (endpoints):
- /auth - валидация пользователя и предоставление ключа (token)
- /user/salary - предоставление информации о ЗП при наличии действительного ключа (token) пользователя
- /user/salary/next_raise_dt - предоставление даты следующего повышения ЗП при наличии действительного ключа (token) пользователя

## /auth:

В случае валидных данных пользователя возвращает токен валидации - в противном случае возвращает ошибку: 401 Unauthorized - "Invalid user credentials".

Входные данные:
- username: str - логин пользователя
- password: str - пароль пользователя

Возвращает:
- access_token: str - ключ пользователя
- token_type: str - "bearer"


Пример:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/auth' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=e0001&password=1&scope=&client_id=&client_secret='
	
Response body:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImUwMDAxIiwiZXhwIjoxNzE1MTg2MzQ5fQ.t_L-aC4MXghNMZc3TC9NNdQ0DRVDSrhFTCa2ajchtVA",
  "token_type": "bearer"
}
```

## /user/salary

В случае валидного ключа пользователя (auth token) возвращает текущее значение ЗП - в противном случае возвращает ошибку: 401 Unauthorized - "Invalid JWT".
В случае если отсутствуют данные по ЗП - возвращает null.

Входные данные:
- Header(Authorization): str = "Bearer" + token

Возвращает:
- float


Пример:

```
curl -X 'GET' \
  'http://127.0.0.1:8000/user/salary' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImUwMDAyIiwiZXhwIjoxNzE1MTg3ODk4fQ.hYwrU0T8MsJdOsi99OiID8phZLyLRIeL6Y0wA8E2weQ'
	
Response body:
10237.99
```

## /user/salary/next_raise_dt

В случае валидного ключа пользователя (auth token) возвращает дату повышения ЗП - в противном случае возвращает ошибку: 401 Unauthorized - "Invalid JWT".
В случае если данные отсутствуют - возвращает null.

Входные данные:
- Header(Authorization): str = "Bearer" + token

Возвращает:
- str (UTC datetime)


Пример:

```
curl -X 'GET' \
  'http://127.0.0.1:8000/user/salary/next_raise_dt' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImUwMDAyIiwiZXhwIjoxNzE1MTg4OTA3fQ.DUzkBYZ9LD5TSxy9fmdzHvGrB5oHmD2rtVAtnNfGCMc'
	
Response body:
"2024-09-01 00:00:00"
```

## Запуск API:

API запускается при выполнении файла main.py.

API доступно по http://127.0.0.1:8000 либо по http://localhost:8000.

В качестве тестовых данных были добавлены следующие записи:
- login: e0001, password: 1, salary: 1, next_raise_dt: "2027-01-01T00:00:00"
- login: e0002, password: 2, salary: 10237.99, next_raise_dt: "2024-09-01T00:00:00"
- login: e0002, password: 3, salary: null (None), next_raise_dt: null (None)

Для тестирования в ручном режиме можно использовать Swagger UI (http://127.0.0.1:8000/docs# либо http://localhost:8000/docs#).


## Docker:

Создание docker image:
```
docker build -t shift-61548 .
```

Запуск контейнера:
```
docker run -dp 127.0.0.1:8000:8000 shift-61548
```


