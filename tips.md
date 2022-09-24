# TIPS

Адрес тестовой среды ( далее `{{domain}}` ):
https://api.yii2-stage.test.wooppay.com

---
## Дополнительные данные

На тестовой и производственной средах будут использоваться следующие данные:

- **Partner-name:** `tips` - использовать при работе с js-call;
- **Partner-name:** `tips_p` - использовать при работе с PostMessage;
- **Префикс субъектов:** `TP`.

---
### Сценарий:

1. Официант:

- Я как официант регистрируюсь

- Создаю сервис доната

- Могу получать донаты

- Могу просматривать историю донатов

- Могу делать выводы на карту, но после идентификации

2. Посетитель:

- Я как посетитель могу давать чаевые с карты (оплачивать сервис-донат)

<a name="home"></a>
### Содержание:

1. [Авторизация](#auth)
2. [Регистрация новых пользователей](#reg)
    - [Регистрация новых пользователей самим пользователем](#regByUser)
3. [Баланс кошелька](#balance)
    - [Запрос баланса кошелька](#getBalance)
4. [Вывод на карту](#withdrawal)
5. [Запрос статуса и чека (В виде данных и в формате PDF)](#receipt)
    - [Просмотр чека об операции](#receiptSimple)
    - [Запрос чека об операции в формате pdf](#receiptPdf)
6. [Работа с историей](#history)
7. [Запрос статуса операции](#operation_status)
8. [Создание услуги-доната](#createService)
9. [Запрос доступных услуг-донатов](#createService)
10. [Запрос списка полей и валидаторов для сервиса](#getFieldsnValidators)
11. [Оплата услуг](#pay)
12. [Работа с js-call и postMessage](#frame)
13. [Идентификация](#ident)
14. [Коды ошибок и прочее](#other)

-------

<a name="auth"></a>
## 1. Авторизация

**POST**: `{{domain}}/v1/auth`

**Params:** -

**Headers:**

| Параметр  |  Значение |
|----------|-------------|
| Content-Type | application/json |
| language | ru (по умолчанию) |
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) |


**Body:**

| Параметр | Тип|  Описание |
|------|-------|--------------|
| login   |    string| *Логин субъкта* |
| password   |  string |*Пароль* |


**Возвращаемые параметры:**

| Параметр     | Тип    | Описание                          |
| ------------ | ------ | --------------------------------- |
| parent_login | string | *Логин родительского субъекта*    |
| subject_type | int    | *Тип авторизованного субъекта  в сисстеме WOOPPAY*    |
| country      | int    | *ID страны*                       |
| id           | int    | *ID авторизованного субъекта*     |
| login        | string | *Логин авторизованного субъекта*  |
| status       | int    | *Статус авторизованного субъекта* |
| roles        | массив со string внутри | *Роли авторизованного субъекта в сисстеме WOOPPAY* |
| assignments  | string | *Внутренняя система ролей*        |
| token        | string | *[Авторизационный токен](#token)* |
| email        | string | *Почта авторизованного субъекта*  |
| created_at   | string | *Дата и время авторизации*        |
| identified   | int    | *Идентификация*                   |
| resident_kz  | string | *Резидент РК*                     |


<a name="token"></a>

**Пример запроса:**
```json  
    {
    	"login":"login",
    	"password":"password"
    }
```

**Пример успешного ответа:**

`HTTP status code: 200 OK` - _Успешно. Запрошенный ресурс был найден и передан в теле ответа_
``` json
    {
        "parent_login": null,
        "subject_type": 2000,
        "country": 4,
        "id": 123456,
        "login": "login",
        "status": 1,
        "roles": [
            "someRole",
            "someRole1"
        ],
        "assignments": null,
        "token": "jwt eyJraWQiOiJr..",
        "email": null,
        "created_at": "2019-05-29T05:01:12+0000"
        "identified": 2,
        "resident_kz": true
    }
```

 > Параметр "token" - сгенерированный авторизационный токен. Предназначен для последующих запросов.

*Авторизационный токен:*  

```json

    "token": "jwt eyJraWQiOiJr.."

```

-------
<a name="reg"></a>
## 2. Регистрация новых пользователей

[_Регистрация пользователем.(Когда пользователь совершает регистрацию сам)_](#regByUser)

-----
<a name="regByUser"></a>
#### 2.1 Регистрация пользователем

Регистрация новых пользователей происходит в 2 шага:

1. [Создание пользователя](#createUser);
2. [Активация пользователя](#activateUser).

-------
<a name="createUser"></a>
##### 1. Создание пользователя

**POST:** `{{domain}}/v1/registration/create-account`

**Params:** -

**Headers:**

| Параметр | Значение |
|----------|-------------|
| Content-Type |application/json |
| language | ru (по умолчанию) |
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) |
| Partner-name | Имя партнера |

**Body:**

| Параметр | Тип|  Описание |
|------|-------|-------------|
| login   |    string |  *Логин субъекта (Телефон)* |
| email   |  string |*E-mail* |


**Возвращаемые параметры:**

Если все прошло удачно - в ответ получаем пустой массив, статус ответа - `201 Created`


**Пример запроса:**
```json   
    {
    	"login": "77758408303",
    	"email": "example@example.com"
    }
```

**Пример успешного ответа:**

`HTTP status code: 201 Created` - _Успешно.Субъект был создан_
``` json
    null
```
На указанный номер - придет СМС-сообщение с КОДом активации пользователя

----
<a name="activateUser"></a>
##### 2. Активация пользователя

**POST:** `{{domain}}/v1/registration/set-password`

**Params:** -

**Headers:**

| Параметр  |  Значение |
|----------|-------------|
| Content-Type|application/json
| language     | ru (по умолчанию)
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) |
| Partner-name | Имя партнера |

**Body:**

| Параметр | Тип |  Описание |
|------|-------|-------------|
| login   |    string |  *Логин субъекта* |
| password   |  string |*Пароль* |
| activation_code | integer | *КОД из смс-сообщения. В тестовой среде - 111111* |
**Возвращаемые параметры:**

Если все прошло удачно - в ответ получаем пустой массив, статус ответа - `201 Created`


**Пример запроса:**
```json   
    {
    	"login": "77758408303",
    	"password": "Password",
    	"activation_code": "111111"
    }
```

**Пример успешного ответа:**

`HTTP status code: 201 Created` - _Успешно.Субъект был создан_
``` json
    []
```

-------
<a name="balance"></a>

## 3. Баланс кошелька

1. [Запрос баланса кошелька](#getBalance).

-----
<a name="getBalance"></a>

#### 3.1 Запрос баланса кошелька

**GET:** `{{domain}}/v1/balance`

**Headers:**

| Параметр | Значение |
|----------|------------|
| Authorization| *[Авторизационный токен](#token)* |
| Content-Type | application/json |
| Language | ru (по умолчанию) |
| Time-Zone|  Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) |
| Partner-name | Имя партнера |

**Возвращаемые параметры:**

| Параметр | Тип    | Описание |
|---------|--------|------------|
| active  | int  | Доступные средства |
| blocked | int | Средста находящиеся в блоке |
| acc_base | int | Сумма доступных средств и средств находящихся в блоке |
| acc_commission | int | Комиссия |

**Пример запроса:**

**GET:** `{{domain}}/v1/balance`


**Пример успешного ответа:**

`HTTP status code: 200 OK` - _Успешно._

``` json
    {
        "active": 10980,
        "blocked": 14224,
        "acc_base": 25204,
        "acc_commission": 0
    }

```

-------

<a name="withdrawal"></a>
## 4. Вывод на карту

**ВНИМАНИЕ! Вывод на карту доступен только [идентифицированным](#ident) пользователям**


**POST:** `{{domain}}/v1/payment/transfer-to-card`

**Headers:**

| Параметр  |  Значение |
|----------|------------|
| Authorization|  *[Авторизационный токен](#token)* |
| Content-Type | *application/json* |
| Language | *ru (по умолчанию)* |
| Time-Zone |  *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)*
| Partner-name | *Имя партнера* |

**Body:**

| Параметр | Тип    | Описание |
|---------|--------|-----------|
| amount | float | *Сумма вывода* |
| *[mobile_scripts](#frame)* | boolean | *Запуск скриптов false/true* |

**Возвращаемые параметры:**


| Параметр | Тип    | Описание |
|---------|--------|-----------|
| frame_url  | string  | *Ссылка на ввод карточных данных* |
| operation_id | int | *Идентификатор операции в системе* |


**Пример запроса:**

**POST:** `{{domain}}/v1/payment/transfer-to-card`

```json
{
    "amount": "1000",
    "mobile_scripts": true
}
```


**Пример успешного ответа:**

`HTTP status code: 200 OK` - _Успешно._


``` json
    {
        "frame_url": "https://pci-ws.wooppay.com/cashout/input?Uid=84090230-322a-4ef8-aad5-b0bcabe3a9cf",
        "operation_id": 476877225
    }
```

-------

<a name="receipt"></a>
## 5. Запрос статуса и чека операции

1. [Просмотр чека об операции](#receiptSimple)
2. [Запрос чека об операции в формате pdf](#receiptPdf)

-------
<a name="receiptSimple"></a>
### 5.1 Просмотр чека об операции
Если оплата прошла успешно, статус операции 14 - _"Проведена"_. Описание статусов операций доступны в конце документа.
Запрос статуса операции и чека происходит запросом метода:

**GET** `{{domain}}/v1/history/receipt/50862733`,

> где: 50862733 - ID платежа,

**Входные параметры:**

**Headers:**

|Параметр  |  Значение |
|----------|------------|
| Content-Type | application/json  |
| Authorization |  *[Авторизационный токен](#token)*|
| Language     | ru (по умолчанию) |
| Partner-name | *Имя партнера* |
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) |


**Возвращаемые параметры:**


| Параметр | Тип    | Описание |
|---------|--------|-------------|
| id    |  int   | ID операции |
| operator_title    |  string   | Юридическое имя оператора |
| operator_bin    |  int   |БИН оператора |
| login    |  int   | Логин |
| time    |  string   | Время проведения платежа |
| merchant_title    |  string   | Юридическое имя мерчанта |
| merchant_bin    |  int   | БИН мерчанта |
| service_title   |   string   |    Название сервиса |
| ident:    |  массив с объектами json | Поля с данными |
<ol><li>title</li><li>value</li></ol>    |  <ol><li>string</li><li>string</li></ol>  | <ol><li>Название поля</li><li>Значение поля</li></ol> |
| amount    |  float   | Сумма платежа |
| commission    |  float   | Комиссия |
| admit    |  float   |  Сумма, на которую пополнится счет |
| vat    |  float   | НДС |
| emitent    |  string   | Имя эмитента |
| agent    |  string   | Имя специалиста |
| operation_type    |  int   | Тип операции |
| transaction    | объект json   | Поля с данными |
<ol><li>status</li><li>type</li></ol>    |  <ol><li>int</li><li>int</li></ol>   | <ol><li>Статус операции</li><li>Тип операции</li></ol> |
| linked_operations    |  Массив со string внутри   | Операции, связанные с данной операцией |


**Пример запроса:**

**GET:** `{{domain}}/v1/history/receipt/50862733`

**Пример успешного ответа:**

`HTTP status code: 200 OK` - _Успешно._

```json
    {
        "id": 50862733,
        "operator_title": "ТОО \"WOOPPAY\" (ВУППЭЙ)",
        "operator_bin": "120340004314",
        "login": "77780623250",
        "time": "2020-04-30T14:27:11+0600",
        "merchant_title": "voyage-krg.kz ",
        "merchant_bin": "120940013632",
        "service_title": "Kcell",
        "ident": [
            {
                "title": "Внешний ID",
                "value": "20200430082531161000"
            },
            {
                "title": "Номер телефона",
                "value": "7012115207"
            }
        ],
        "amount": 10,
        "commission": 0,
        "admit": 10,
        "vat": 0,
        "emitent": "Банк Анвара ручное",
        "agent": "kcell_sub ",
        "operation_type": 300,
        "transaction": {
            "status": 14,
            "type": 300
        },
        "linked_operations": [
            "50862735"
        ]
    }
```


Пример запроса чека со статусом 12 - _"На рассмотрении"_

**Пример запроса:**

**GET:** `{{domain}}/v1/history/receipt/50349355`


**Пример ответа:**

```json
    {
        "id": 50349355,
        "transaction": {
            "status": 12,
            "type": 205
        }
    }
```

-------
<a name="receiptPdf"></a>
### 5.2 Запрос чека об операции в формате pdf

**GET:** `{{domain}}/v1/history/receipt/pdf/50347630`,


> где: 50347630 - ID операции

**Headers:**

| Параметр  |  Значение |
|----------|------------|
|Authorization|  *[Авторизационный токен](#token)* |
|Content-Type | *application/json* |
| Language     | *ru (по умолчанию)* |
| Partner-name | *Имя партнера* |
| Time-Zone | *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |



**Возвращаемые параметры:**

    Возможность скачать чек в формате PDF

-------
<a name="history"></a>

## 6. Работа с историей

**GET:** `{{domain}}/v1/history`

Для метода доступна пагинация и в заголовках возвращаются данные по количеству элементов на страницу и количество странице

**Пример:**
```JSON
X-Pagination-Total-Count: 59
X-Pagination-Page-Count: 6
X-Pagination-Per-Page: 10
X-Pagination-Current-Page: 1
```
**Исходя из примера мы видим:**

| Параметр     | Значение          |
| ------------ | ----------------- |
| X-Pagination-Total-Count | Количество элементов (Всего) - из примера - 59  |
| X-Pagination-Page-Count     | Количество страниц (Всего) - из примера - 6 |
| X-Pagination-Per-Page | Количество элементов на странице - из примера - 10 |
| X-Pagination-Current-Page | Текущая страница |

Исходя из этих данных можно настроить приложение и плавно подгружать элементы на странице в приложении.

**Params:**

| Параметр     | Значение  |
| ------------|----------|
| done_from | Выбор начальной даты отсчета(формат ГГГГ-ММ-ДД) |
| done_to     | Выбор конечной даты отсчета(формат ГГГГ-ММ-ДД) |
| per-page | Установить количество записей на странице |
| expand{service.fields} | Вложенность данных по сервису, полям |
| status | Статусы операций |
| type| Типы операций |
| page | Страница |

**Headers:**

| Параметр     | Значение          |
| ------------ | ----------------- |
| Content-Type | application/json  |
| Authorization | [Авторизационный токен](#token) |
| Language     | ru (по умолчанию) |
| Partner-name | *Имя партнера* |
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) |



**Возвращаемые параметры:**


| Параметр | Тип | Описание |
|---------|--------|--------|
| id | int   | *ID операции* |
| amount | float | *Сумма* |
| service_id   |   int   | *ID сервиса* |
| external_id    |  int   | *Внешний ID* |
| created_at| string | *Дата создания операции* |
| donned_at | string | *Дата окончания проведения платежа* |
| id | int | *ID сервиса* |
| name | string | *Имя сервиса* |
| parent_id    | int  | *ID сервиса или ID категории* |  
| title  | string | *Название* |
| description   | string  | *Описание сервиса* |
| description_company  | string  | *Описание компании* |
| commission_info   | string  | *Информация о комиссии* |
| picture   | string  | *Иконка* |  
| synonyms   | string  | *Синонимы для поиска* |
| type   | int | *Тип сервиса(в данном случае биллинг)* |
| status   | int  | *Статус сервиса(см. в конце документа)* |
| template   | string  | *Шаблон сервиса* |
| is_simple   | boolean | *Если у сервиса есть кнопка, то fasle. Кнопка определяет процесс проведения операции в биллинге* |
| priority | int  | *Позиция сервиса по списку - чем выше число, тем приоритетнее* |
| updated_at   | string  | *Последнее обновление информации по сервису* |
| categories:   | массив с объектами json  | *Список категорий, где находится данный сервис* |
| children:   | string  | *Список дочерних сервисов* |
| picture_url   | string  | *Ссылка на лого сервиса* |
| blacklist   | boolean  | *Запрещен ли этот сервис* |
| parent   | string  | *Объект родительского сервиса или категории* |



**Пример запроса:**

**GET:** `{{domain}}/history?done_from=2020-06-24&done_to=2020-07-01&expand=service.fields&status=12,14,19&type=100,200,201,202,203,204,205,206,230,233,300,304,330,334&per-page=15&page=1`


**Пример успешного ответа:**

```json
     [
         {
            "id": 476877225,
            "parentId": 0,
            "amount": 1030,
            "status": 14,
            "direction": "outgoing",
            "type": 205,
            "title": "Вывод на карту",
            "description": null,
            "account": "417660-XX-XXXX-7215",
            "service_id": 1393,
            "external_id": null,
            "created_at": "2021-02-10T13:13:02+0000",
            "donned_at": "2021-02-10T13:13:10+0000",
            "receipt": null,
            "values": {
                "amount": 1000,
                "service_id": 1393
            },
            "service": {
                "id": 1393,
                "name": "wp_withdrawal",
                "parent_id": null,
                "title": "Вывод на карту",
                "description": "",
                "description_company": "",
                "instruction": "",
                "commission_info": "",
                "picture": "service599e757c18e123.76457945.png",
                "synonyms": [
                    "вп_витхдравал"
                ],
                "type": 9,
                "terminal_type": null,
                "status": 0,
                "template": null,
                "is_simple": true,
                "priority": 0,
                "updated_at": "2019-08-29T10:21:43+0000",
                "fields": [
                    {
                        "id": 4832,
                        "service_id": 1393,
                        "name": "amount",
                        "type": "amount",
                        "sort": 0,
                        "hidden": false,
                        "button": false,
                        "readonly": false,
                        "mask": "",
                        "unmask": true,
                        "value": null,
                        "steps": [
                            1,
                            2,
                            3
                        ],
                        "validations": [],
                        "values": [],
                        "blacklist": null,
                        "button_title": null,
                        "is_need_send": true,
                        "title": "Сумма"
                    },
                    {
                        "id": 4833,
                        "service_id": 1393,
                        "name": "txn_id",
                        "type": "string",
                        "sort": 1,
                        "hidden": true,
                        "button": false,
                        "readonly": false,
                        "mask": "",
                        "unmask": true,
                        "value": null,
                        "steps": [
                            1,
                            2,
                            3
                        ],
                        "validations": [],
                        "values": [],
                        "blacklist": null,
                        "button_title": null,
                        "is_need_send": false,
                        "title": null
                    }
                ],
                "categories": null,
                "children": null,
                "parent": null,
                "blacklist": false,
                "country_code": 1,
                "acquiring_access": 0,
                "params": null,
                "subject": null,
                "fast_input": "",
                "picture_url": "https://static.test.wooppay.com/service/service599e757c18e123.76457945.png"
            }
        }
    ]
```

-------
<a name="operation_status"></a>
## 7. Запрос статуса операции

Если оплата прошла успешно, статус операции `14 | Проведена`

Запрос статуса операции происходит методом  запроса


**POST:** `{{domain}}/v1/history/transaction/get-operations-data`

**Headers:**

| Параметр  | Значение |
|----------|------------|
| Content-Type | *application/json*  |
| Authorization |  *Авторизационный токен*|
| Language     | *ru (по умолчанию)* |
| Time-Zone | *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |

**Body:**

| Параметр  |  Значение |
|----------|------------|
| operation_ids | *Массив с идентификаторами операций*  |

**Возвращаемые параметры:**

| Параметр | Описание |
|---------|-------------|
| operation_id | *ID операции* |
| status    | *Статус операции* |
| amount    | *Сумма с учетом комиссии* |
| external_id | *Внешний ID операции (может быть равен 0 и null)* |

**Возможные статусы операций**

| Статус | Описание |
|----------|--------|
| 11 | *Новая* |
| 12 | *На рассмотрении* |
| 14 | *Проведена* |
| 17 | *Отменена* |
| 19 | *Ожидает проведения* |
| 20 | *Удалена* |

**Пример запроса:**

**POST:** `{{domain}}/v1/history/transaction/get-operations-data`

```json
{
  "operation_ids": [
    "50943267",
    "50943264"
  ]
}
```

**Пример ответа:**

```json
[
    {
        "operation_id": 50943264,
        "status": 14,
        "amount": 1100,
        "external_id": "1605062851"
    },
    {
        "operation_id": 50943267,
        "status": 11,
        "amount": 1100,
        "external_id": "1605063126"
    }
]
```

---------

<a name="createService"></a>
## 8. Создание услуги-доната

Создание услуги-доната происходит методом **POST** запроса


**URL:** `{{domain}}/v1/service/donate`


**Входные параметры:**

**Headers:**


|Параметр  |  Значение | Обязательность |
|----------|------------|-------|
| Content-Type | application/json  | + |
| Authorization |  *Авторизационный токен* | + |
| Language     | ru (по умолчанию) | - |
| Partner-name | *Имя партнера* | - |
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) | - |

**Body:**

|Параметр  |  Описание | Обязательность |
|----------|------------|-------|
| title | *Заголовок*  | - |
| name |  *Имя услуги* | + |
| description | *Описание услуги* | - |
| fields{amount} | *Сумма. Если указать 0 или не передать - то клиент может передать произвольное значение. Если указать конкретную сумму - то клиент сможет оплатить только заданную сумму* | + |

**Пример запроса**

```json
{
    "fields": {
        "amount": "0"
    },
    "title" : "Чаевые!",
    "name": "УРА! Чаевые!",
    "description" : "Нужно больше золота..."
}
```



**Пример успешного ответа:**

HTTP status code: 200 OK - Успешно. Запрошенный ресурс был найден и передан в теле ответа

```json
{
    "service_name": "transfer_***"
}
```

**Возвращаемые параметры:**

| Параметр | Описание | 
|---------|------------|
| service_name | *Системное имя сервиса* |

----------

<a name="getService"></a>
## 9. Запрос доступных услуг-донатов

-----------
Запрос доступных услуг-донатов происходит методом **GET** запроса


**URL:** `{{domain}}/v1/service/donate`


**Входные параметры:**

**Headers:**


|Параметр  |  Значение | Обязательность |
|----------|------------|-------|
| Content-Type | application/json  | + |
| Authorization |  *Авторизационный токен* | + |
| Language     | ru (по умолчанию) | - |
| Partner-name | *Имя партнера* | - |
| Time-Zone | Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty) | - |

**Пример запроса**

GET: `{{domain}}/v1/service/donate`



**Пример успешного ответа:**

HTTP status code: 200 OK - Успешно. Запрошенный ресурс был найден и передан в теле ответа

```json
[
    {
        "service_name": "transfer_454655",
        "name": "Перевод пользователю tetetet"
    },
    {
        "service_name": "transfer_77052507047_1663656788",
        "name": "transfer_77052507047_1663656788"
    },
    {
        "service_name": "transfer_77052507047_1663656802",
        "name": "transfer_77052507047_1663656802"
    }
]
```


**Возвращаемые параметры:**

| Параметр | Описание | 
|---------|------------|
| service_name | *Системное имя сервиса* |
| name | *Заголовок, имя сервиса* |


----------
<a name="getFieldsnValidators"></a>
## 10. Запрос списка полей и валидаторов для сервиса
---------------

Запрос списка полей и валидаторов сервиса происходит методом **GET** запроса


**URL:** `{{domain}}/v1/service/{{service_name}}?status=4&expand=params,fields,fields.validations`

где: {{service_name}} - название сервиса




У каждого поля есть признаки:

1. Скрытое - hidden

2. Шаги, на которых данное поле используется

        "steps": [
            1,
            2,
            3
        ]
Исходя из этих признаков, можно понять, когда данное поле используется и отображается.
По шагам:
```json
 1 - Первый шаг, на начале отображения для пользователя,
 2 - check,
 3 - pay
```

3. Есть еще логика с шаблоном debtinfo (как правило ком услуги с запросом квитанций):

        "name": "amount",
        "type": "amount_group"
        "hidden": true,
Группа сумм - скрыта до тех пор, пока не придет квитанция. Как приходит квитанция, на уровне интерфейса вырисовывается группа сумм, исходя из данных по квитанции (Вода, газ, свет и т.д. )

4. Шаблон taxInfo: при запросе данных в биллинг возвращается набор контрактов с предустановленой ценой по контрактам.

5. Шаблон balanceInfo: при запросе данных в биллинг возвращается доступный баланс или задолженность указанного счета.  

 В дальнейшем планируется добавление других шаблонов.




**Входные параметры:**

**Headers:**

| Параметр     | Значение          |
| ------------ | ----------------- |
| Content-Type | *application/json*  |
| Authorization| *Авторизационный токен* |
| Language     | *ru (по умолчанию)* |
| Time-Zone | *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |
| Partner-name | *Имя партнера* |


**Пример успешного ответа:**

HTTP status code: 200 OK - Успешно. Запрошенный ресурс был найден и передан в теле ответа

```JSON
{
    "id": 2712,
    "name": "transfer_454655",
    "parent_id": null,
    "title": "Перевод пользователю 77017197535",
    "description": "cfgvbdxf",
    "description_company": null,
    "instruction": null,
    "commission_info": "Комиссия за оплату не взимается",
    "picture": null,
    "synonyms": [],
    "type": 11,
    "terminal_type": null,
    "status": 4,
    "template": null,
    "is_simple": true,
    "priority": 0,
    "updated_at": "2022-07-08T15:32:35+0000",
    "fields": [
        {
            "id": 6889,
            "service_id": 2712,
            "name": "amount",
            "type": "amount",
            "sort": 100,
            "hidden": false,
            "button": false,
            "readonly": true,
            "mask": null,
            "unmask": true,
            "value": "100",
            "steps": [
                1,
                2,
                3
            ],
            "validations": [
                {
                    "id": 5705,
                    "field_id": 6889,
                    "type": "required",
                    "param": {
                        "message": "Заполните поле"
                    }
                },
                {
                    "id": 5706,
                    "field_id": 6889,
                    "type": "compare",
                    "param": {
                        "strict": false,
                        "message": "Невалидное значение",
                        "operator": "=",
                        "allowEmpty": false,
                        "compareValue": "100",
                        "compareAttribute": null
                    }
                }
            ],
            "values": [],
            "blacklist": null,
            "button_title": null,
            "is_need_send": true,
            "title": "Сумма перевода"
        }
    ],
    "categories": null,
    "children": null,
    "parent": null,
    "blacklist": false,
    "country_code": 1,
    "acquiring_access": 1,
    "params": {
        "service_id": 2712,
        "banner_img": "",
        "banner_link": "",
        "back_url": null,
        "request_url": null,
        "page_background_color": "",
        "page_background_url": ""
    },
    "subject": null,
    "fast_input": "",
    "picture_url": null
}
```


**Возвращаемые параметры:**

|   Параметр   |  Тип   |  Описание |
| ------------ | ------ | --------- |
|    id    | int  | ID сервиса  |
|    name    | string  | Системное имя сервиса  |
|    parent_id    | int  | ID сервиса или ID категории  |
|   title  | string  | Название  |
| description   | string  | Описание сервиса  |
|description_company  | string  | Описание компании  |
| commission_info   | string  | Информация о комиссии |
| picture   | string  | Иконка  |
| synonyms   | массив со string внутри  | Синонимы для поиска |
| type   | int  | Тип сервиса(В данном случае биллинг) |
| status   | int  | Статус сервиса(см. в конце документа) |
| template   | string  | Нужно запросить квитанцию по задолженности и сценарий его получения |
| is_simple   | boolean  | Если у сервиса есть кнопка, то fasle. Кнопка определяет процесс проведения операции в биллинге  |
| priority   | int  | Позиция сервиса по списку - чем выше число, тем приоритетнее
| updated_at   | string  | Последнее обновление информации по сервису  |
| categories:   | массив с объектами json  | Список категорий, где находится данный сервис  |
| children:   | string  | Список дочерних сервисов |
| parent:   | string  | Объект родительского сервиса или категории  |
| blacklist:   | boolean  | Запрещен ли этот сервис  |
| picture_url:   | string  | Ссылка на лого сервиса  |
| fields:   | массив с объектами json  | Список полей для оплаты  |
| <ol><li>id</li><li>service_id</li><li>name</li><li>type</li><li>sort</li><li>hidden</li><li>button</li><li>readonly</li><li>mask</li><li>unmask</li><li>value</li><li>steps</li> <li>values</li><li>is_need_send</li> </ol>  |   <ol><li>int</li><li>int</li><li>string</li><li>string</li><li>int</li><li>boolean</li><li>boolean</li><li>boolean</li><li>string</li><li>boolean</li><li>string</li><li>массив с int</li><li>string</li><li>boolean</li></ol> | <ol><li>Идентификатор поля в таблице всех полей в базе Wooppay</li><li>Принадлежность к сервису</li><li>Системное имя поля</li><li>Тип данных внутри поля</li><li>Позиция при отображении(выше/ниже). 0 - выше</li><li>Маркер - скрывать его или нет, false - не скрывать</li><li>Если false - не является кнопкой при отображении</li><li>Если false - запрет на редактирование поля при отображении</li><li>Маска для удобочитаемости поля</li><li>Не учитывать маску при валидации</li><li>Значение по умолчанию</li><li>Шаги оплаты, в которых участвует сервис</li><li>Параметры выпадающего списка, если поле является таковым</li><li>Поле, которое нужно заполнить и отправить в ядро</li></ol>  |
| validations:   | массив с json объектами  | Массив полей  |
| <ol><li>id</li><li>field_id</li><li>type</li></ol>   | <ol><li>int</li><li>int</li><li>string</li></ol>  | <ol><li>Идентификатор валидатора поля в таблице всех валидаторов полей в базе Wooppay</li><li>Принадлежность к полю сервиса</li><li>Тип валидатора(см. в конце документа)</li></ol>  |
| param:   |объект json  | Уточнение по валидатору  |
| <ol><li>message</li><li>pattern</li><li>allowEmpty</li><li>is</li><li>max</li><li>min</li><li>tooLong</li><li>encoding</li><li>tooShort</li><li>tooBig</li><li>tooSmall</li><li>numberPattern</li><li>integerPattern</li></ol>   | <ol><li>string</li><li>string</li><li>int</li><li>int</li><li>int</li><li>int</li><li>string</li><li>boolean</li><li>string</li><li>string</li><li>string</li><li>string</li><li>string</li></ol>   | <ol><li>Сообщение об ошибке, которое отобразится, если поле не пройдет ЭТОТ валидатор</li><li>Шаблон, которому должно соответствовать содержание поля</li><li>Допущение того, что поле может быть пустым, но если есть валидатор required, не имеет смысла</li><li>Поле должно содержать определенное количество символов</li><li>Максимальное количество символов</li><li>Минимальное количество символов</li><li>Сообщение, если слишком длинное значение</li><li>Кодировка</li><li>Сообщение, если слишком короткое значение</li><li>Сообщение, если слишком большое значение</li><li>Сообщение, если слишком маленькое значение</li><li>В системе нужно для определения валидации на случай, если число не просто целое, а с плавающей точкой</li><li>В системе нужно для определения валидации на случай, если число целое</li></ol> |

-------
<a name="pay"></a>
## 11. Оплата услуг

-------
## Оплата услуги-доната


>Сценарий оплаты:

>1. [Псевдоавторизация](#authpS)
>2. [Создание операции доната](#donateS)
>3. [Создание пополнения и подтверждение доната](#pay_from_cardS)


<a name="authpS"></a>
### Псевдоавторизация

Псевдоавторизация происходит методом **POST** запроса

**URL:** `{{domain}}/v1/auth/pseudo`

**Входные параметры:**

**Headers:**

| Параметр  |  Значение |
|----------|-------------|
| Content-Type | *application/json* |
| Language | *ru (по умолчанию)* |
| Time-Zone |  *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |
| Partner-name| *Имя партнера* |

**Body:**

| Параметр | Тип    | Описание |
|---------|--------|-----------|
| login | string | *Номер телефона* |

**Возвращаемые параметры:**

| Параметр     | Тип    | Описание                          |
| ------------ | ------ | --------------------------------- |
| parent_login | string | *Логин родительского субъекта*    |
| subject_type | int    | *Тип авторизованного субъекта  в сисстеме WOOPPAY*    |
| country      | int    | *ID страны*                       |
| id           | int    | *ID авторизованного субъекта*     |
| login        | string | *Логин авторизованного субъекта*  |
| status       | int    | *Статус авторизованного субъекта* |
| roles        | массив со string внутри | *Роли авторизованного субъекта в сисстеме WOOPPAY*   |
| assignments  | string | *Внутренняя система ролей*        |
| token        | string | *[Авторизационный токен](#token)*|
| email        | string | *Почта авторизованного субъекта*  |
| created_at   | string | *Дата и время авторизации*        |
| identified   | int    | *Идентификация*                   |
| resident_kz  | string | *Резидент РК*                     |

\*Использовать полученный **txn_id** для последующих запросов

**Пример запроса:**
```json
{
    "login": "77717441718"
}}
```

**Пример успешного ответа:**

`HTTP status code: 200 OK` - _Успешно. Запрошенный ресурс был найден и передан в теле ответа_
``` json
    {
        "parent_login": null,
        "subject_type": 2000,
        "country": 4,
        "id": 123456,
        "login": "login",
        "status": 1,
        "roles": [
            "someRole",
            "someRole1"
        ],
        "assignments": null,
        "token": "jwt eyJraWQiOiJr..",
        "email": null,
        "created_at": "2019-05-29T05:01:12+0000"
        "identified": 2,
        "resident_kz": true
    }
```

 > Параметр "token" - сгенерированный авторизационный токен. Предназначен для последующих запросов.

*Авторизационный токен:*  

```json

    "token": "jwt eyJraWQiOiJr.."

```

<a name="donateS"></a>
### Создание операции доната

Проверка данных оплаты происходит методом **POST** запроса

**URL:** `{{domain}}/v1/payment/transfer-new`

**Входные параметры:**

**Headers:**

| Параметр  |  Значение |
|----------|-------------|
| Authorization|  *Авторизационный токен* |
| Content-Type | *application/json* |
| Language | *ru (по умолчанию)* |
| Time-Zone |  *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |
| Partner-name| *Имя партнера* |

**Body:**

| Параметр | Тип    | Описание |
|---------|--------|-----------|
| service_name | string | *Системное имя сервиса* |
| fields | объект JSON| *Поля с данными* |
| amount | float | *Сумма платежа* |



**Возвращаемые параметры:**

| Параметр | Тип    | Описание |
|---------|--------|-----------|
| operation {id} | int | *ID операции доната* |

\*Использовать полученный **txn_id** для последующих запросов

**Пример запроса:**
```json
{
    "service_name": "transfer_77052507047_1663670118",
    "fields": {
        "amount": "100"
    }
}
```


**Пример успешного ответа:**

HTTP status code: 200 OK - Успешно.


```json
{
    "operation": {
        "id": "1000135104"
    }
}
```

<a name="pay_from_cardS"></a>
### Создание пополнения и подтверждение доната

Оплата с кошелька происходит методом **POST** запроса


**URL:** `{{domain}}/v1/payment/pay-from-card`


**Входные параметры:**

**Headers:**

| Параметр  |  Значение |
|----------|------------|
| Language     | *ru (по умолчанию)* |
| Partner-name | *Имя партнера* |
| Time-Zone | *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |
| Authorization |  *Авторизационный токен* |
| Content-Type | *application/json* |

**Body:**

| Параметр | Тип    | Описание |
|---------|--------|-----------|
| operation_id | int | *ID операции доната* |



**Возвращаемые параметры:**


| Параметр | Тип    | Описание |
|---------|--------|-----------|
| frame_url | string | *url на форму для ввода карточных данных* |
| operation_id | int | *ID операции пополнения* |
| payment_operation | int | *ID операции доната* |

**Пример запроса:**

```json
{
    "operation_id": "1000135104"
}
```

**Пример успешного ответа:**

HTTP status code: 200 OK - Успешно.

```json
{
    "frame_url": "https://api.yii2-stage.test.wooppay.com/v1/card/frame-generator?*****",
    "operation_id": "1000135108",
    "payment_operation": "1000135104"
}
```

-------
<a name="frame"></a>
## 12. Работа с js-call и postMessage

-------
## Оплата простой услуги
При работе с фреймами в приложениях, взаимодействие происходит на нескольких уровнях. Так положительные или отрицательные моменты взаимодействия возможно отловить на таких уровнях:

### *На уровне всплывающего сообщения внутри frame и на уровне JS-CALL:*

1. Ошибка на уровне валидации - визуальная, всплывающее сообщение (Пример: "Введите корректные карточные данные ")

2. Ответ после отправки данных в виде js-call. Для включения важно использовать партнера ```tips``` и в карточных операциях передавать ```"mobile_scripts": true```

```html
js-call://message?data=1 - success - данные ушли на обработку
js-call://message?data=2 - authorisation_error
js-call://message?data=3&error=................ - result_error - ошибка при обработке данных.
js-call://message?data=4 - result_load - возможный промежуточный статус между 1,2 и 3
```

### *На уровне всплывающего сообщения внутри frame и на уровне PostMessage:*

1. Ошибка на уровне валидации - визуальная, всплывающее сообщение (Пример: "Введите корректные карточные данные ")

2. Ответы на уровне PostMessage

Ответы на уровне PostMessage возможно обработать по средствам javascript. Для включения важно использовать партнера ```tips_p``` и в карточных операциях передавать ```"mobile_scripts": false```

### *Пример обработки:*

```html
var functionName = 'rechargeReceiver';
      var frameType = 'recharge';
      var frame_result_load = '4';
      var frame_result_success = '1';
      var frame_result_error = '3';
      var frame_result_authorisation_error = '2';
      var frame_result_form_send = '8';

      if (typeof functionName != "function") {
         functionName = function (event) {
          if (event.data) {
            var message = JSON.parse(event.data);
            if (message && message.source == frameType) {
              var err_info = "";
              if (message.data && typeof message.data.errorCode != "undefined") {
                var errors_text = {"e_04":"Карта заблокирована. Для снятия ограничений, позвоните в Колл-центр вашего банка.","e_05":"Транзакция отклонена. Позвоните в Колл-центр вашего банка.","e_07":"Карта заблокирована. Для снятия ограничений, позвоните в Колл-центр вашего банка.","e_12":"Недействительная транзакция, перепроверьте введенные данные. В случае повторения ошибки попробуйте позже...","e_14":"Недействительный номер карты.","e_15":"Недействительный номер карты.","e_19":"Ошибка авторизации.","e_30":"Переданы неверные данные для оплаты\/пополнения. Обратитесь в службу поддержки.","e_36":"Карта заблокирована. Для снятия ограничений, позвоните в Колл-центр вашего банка.","e_37":"По карте выставлены ограничения. Для снятия ограничений, позвоните в Колл-центр вашего банка.","e_41":"Карта, числится в базе утерянных. Позвоните в Колл-центр вашего банка.","e_43":"Карта, числится в базе утерянных. Позвоните в Колл-центр вашего банка.","e_45":"Карта, числится в базе украденых. Позвоните в Колл-центр вашего банка, либо обратиться в ближайшее отделение полиции.","e_51":"Недостаточно средств на карте.","e_54":"Истёк срок действия карты.","e_57":"Карта закрыта для интернет-транзакций. Обратитесь в ваш банк.","e_58":"Операции с картами временно приостановлены. Попробуйте позже.","e_61":"Сумма превышает допустимый суточный лимит. Можете обратиться в службу поддержки, либо завершить операцию завтра.","e_62":"Карта заблокирована банком. Позвоните в Колл-центр вашего банка.","e_91":"Ваш банк временно не доступен. Попробуйте оплатить позже.","e_96":"Не установлен 3DSecure(SecureCode) либо сбой связи. Позвоните в Колл-центр вашего банка."};
                var err_key = "e_" + message.data.errorCode;
                if(err_key in errors_text){
                  err_info = errors_text[err_key];
                }
              }
              if (message.status == frame_result_load) {
								// место реакции на завершение рендера фрейма
                 window.location = "js-call://message?data=4";console.log("load");
              } else if (message.status == frame_result_success){
//место реакции на событие успешной валидация и отправки карточной формы
    var referenceId = ""
    if ("data" in message){
         referenceId = "referenceId" in message.data ? "&reference=" + message.data.referenceId : "";
    }
    window.location = "js-call://message?data=1" + referenceId;
    console.log("success");
              } else if (message.status == frame_result_error) {
// место реакции на ошибку фрейма
                if (err_info == "") {
                  err_info = "Произошла ошибка. Скорее всего вы ввели некорректные данные карты";
                }
                 window.location = "js-call://message?data=3&error=" + encodeURI(err_info);console.log("err "+encodeURI(err_info));
              } else if (message.status == frame_result_authorisation_error) {
								//место реакции на неверную авторицию фрейма.
                if (err_info == "") {
                  err_info = "Произошла ошибка. Возможно вы ввели некорректные данные карты";
                }
                window.location = "js-call://message?data=2&error=" + encodeURI(err_info);console.log("auth_err "+encodeURI(err_info));
              } else if (message.status == frame_result_form_send) {
								//место реакции на событие отправки формы
               window.location = "js-call://message?data=8&error=" + encodeURI(err_info);console.log("send_err "+encodeURI(err_info));
              }
            }
          }
        };
        window.addEventListener("message", functionName, false);
      }
```

<a name="ident"></a>
## 13. Идентификация

<a name="sc"></a>

#### Возможные сценарии:

**1. Сценарий построенный на основе статуса идентификации кошелька в WOOPPAY.**

Инициализировать идентификацию после запроса статуса идентификации субъекта.

>Пример такого сценария:

>1. Авторизация, отдельный запрос статуса - получаем статус идентификации;
>2. Если кошелек имеет статус идентификации 0 (*"identified": 0*), на уровне интерфейса появляется информация о законе и предложение пройти идентификацию.


**2. Сценарий в случае возникновения ошибок связанных с лимитами неидентифицированных пользователей.**

Ожидаем ошибку с кодом **1196, 1194** со стороны API, реализуем сценарий для идентификации.

>Пример такого сценария:

>1. Пользователь совершает вывод или оплату на сумму превышающую лимиты связанные с идентификацией;
>2. Со стороны API возникает ошибка связанная с лимитами и идентификацией;
>3. На уровне интерфейса появляется ошибка, информация о законе и предложение пройти идентификацию.


**Ошибки связанные с идентификацией со стороны API возникающие при оплате и выводах:**

| Ошибка | Описание | 
|-----|---------|
| 1194 | *Превышение лимита по операции для упрощенно-идентифицированного пользователя* |
| 1196 | *Превышение лимита по операции для не идентифицированного пользователя* |

**Пример ошибки возникающей при оплате и выводах:**

```json
[
    {
        "field": "amount",
        "message": "Ошибка по лимитам операции",
        "error_code": *** 
    }
]
```

---
<a name="statusid"></a>
#### Запрос статуса идентификации субъекта

Получение статуса идентификации субъекта доступно в нескольких местах.

>1. [При авторизации (параметр identified)](#auth)
>2. [При запросе статуса идентификации](#idid)


---
<a name="idid"></a>
### Запрос статуса идентификации кошелька

Запрос статуса идентификации кошелька происходит методом **GET** запроса

**URL:** {{domain}}/v1/user/id-status

**Входные параметры:**

**Headers:**

| Параметр | Значение |
| --- | --- |
| Content-Type | *application/json* |
| Authorization | *[Авторизационный токен](#authtoken)* |
| Language | *ru (по умолчанию)* |
| Partner-name | *Имя партнера* |
| Time-Zone | *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |

**Возвращаемые параметры:**

| Параметр | Описание |
| --- | --- |
| status | *Статус идентификации субъекта* |

**Возможные статусы идентификации:**

| Параметр | Описание |
| --- | --- |
| 0 | *Не идентифицированный субъект* |
| 1 | *Упрощенно идентифицированный субъект* |
| 2 | *Идентифицированный субъект* |

**Пример запроса:**

**GET:** `{{domain}}/v1/user/id-status`

**Пример успешного ответа:**
HTTP status code: 200 OK - Успешно.

```json
{
    "status": 1
}
```

### Генерация уникальной ссылки на анкету для идентификации


Генерация уникальной ссылки на анкету для идентификации происходит методом **POST** запроса


**URL:** `{{domain}}/v1/user/nominate-subject`


**Входные параметры:**

**Headers:**

| Параметр     | Значение          |
| ------------ | ----------------- |
| Content-Type | *application/json*  |
| Language     | *ru (по умолчанию) - В данном методе позволяет открывать анкету с переводом, на нужном языке* |
| Authorization | *[Авторизационный токен](#authtoken)* |
| Time-Zone | *Временная зона - по умолчанию время указано в UTC-0 (Пример: Asia/Almaty)* |
| Partner-name | *Имя партнера* |

**Body:**

| Параметр | Тип|  Описание |
|------|-------|-------|
| phone   | string | *Номер телефона субъекта, для которого требуется уникальная ссылка на анкету для идентификации. Принимает значение от 11 до 14 цифр. Спец символы, буквы - вырезаются* |
| viewType   | string | *Необязательный параметр - позволяет включить скрипты. На данный момент доступно значение frame. При передаче другого значения - проигнорируется* |

**Возвращаемые параметры:**

| Параметр     | Тип    | Описание |
|------------|------|---------------------------------|
| url | string | *Уникальная ссылка на анкету для идентификации* |
| uid | string | *Уникальный идентификатор пользователя*

**Пример запроса**

**POST:** `{{domain}}/v1/user/nominate-subject`

```json
{
  "phone": "77751234567"
}
```


**Пример успешного ответа:**

```json
{
    "url": "https://weblooker.test.wooppay.com/?uid=XXX&phone=77751234567&language=ru&viewType=frame",
    "uid": "XXX"
}
```

**Параметры сформированной ссылки:**

| Параметр | Тип данных\ значение | Описание | Обязательность параметра |
|-----|-----|----|-----|
| uid | string  | *Уникальный идентификатор* | Обязательный |
| phone | string  | *Номер телефона*  | Обязательный |
| viewType | string / frame | *Параметр включает js-call - необходимо для корректной работы внутри webview. Значения ответов при работе с js-call: 0 - ошибка, 1 - успех* | Не обязательный |


**Пример ошибочного ответа:**

```json
[
    {
        "field": "phone",
        "message": "Not valid phone",
        "error_code": 1
    }
]

[
    {
        "field": "technicalError",
        "message": "Ошибка при запросе на идентификацию",
        "error_code": 2201
    }
]
```

Ошибки при генерации уникальной ссылки для идентификации:

| Ошибка | Описание | 
|-----|---------|
| 1 | ERROR_UNKNOWN_ERROR | 
| 2201 | Ошибка при запросе на идентификацию | 
| 2202 | Ошибка при запросе на идентификацию | 
| 3013 | Недостаточно прав для данного действия | 
| 3018 | ERROR_FILE_OPERATION_FAILED |


---

<a name="other"></a>
## 14. Коды ошибок и прочее

#### Тестовые карточные данные

Название поля | Значение
----------|------
Номер карты | *5101459202001215*
Месяц\Год | *10\2026*
CVV | *123*
Имя держателя | *THREED*
3DS | *999999*

Название поля | Значение
----------|------
Номер карты | *5352889914167043*
Месяц\Год | *10\2030*
CVV | *123*
Имя держателя | *THREED*
3DS | *999999*


#### Возможные статусы операций

Статус | Описание
----------|-------------------------------------------------
11 | *Новая*
12 | *На рассмотрении*  
14 | *Проведена*
17 | *Отменена*
19 | *Ожидает проведения*
20 | *Удалена*

#### Статусы сервисов:

Статус | Описание
----------|------
0 | Действующая  
1 | На модерации
2 | Закрытая
3 | Скрытая
4 | Скрытая
5 | Скрытая


#### Типы валидаторов

Тип | Описание
----------|------
match | Соответсвует определенному регулярному выражению.
required | Обязательное к заполнению поле, располагать на стороне клиента. Выйдет ошибка, если не отправить это поле.
length | Определяет максимальную, минимальную, точное соответствие длины поля.


#### Типы операций

Статус | Описание
----------|------
203 | *Пополнение кошелька*
205 | *Выводы*
300 | *Платежи*
304 | *Инвойсы*


#### Коды ошибок error_code

Код | Описание
----------|-------------------------------------------------
1111 | *Превышены лимиты при создании новой операции*
1140 | *Неверный тип операции*
1143 | *Неверный статус операции*  
1156 | *Операция запрещена*
1509 | *Неверный СМС-код*
1510 | *Превышено количество попыток ввода*
1512 | *На балансе недостаточно средств*
1516 | *Номер не зарегистрирован в MFS*
1518 | *Недостаточно средств*
1522 | *Неверный тарифный план*
1604 | *Ошибка взаимодествия с оператором*
1606 | *На балансе недостаточно средств*
1607 | *Номер клиента не найден в системе MFS*
1608 | *Не потрачен стартовый\\бонусный баланс*
1609 | *Неверный тарифный план*
1611 | *Недоступно для юр.лиц*
1612 | *Недоступно для абонентов в роуминге*
1613 | *Данная услуга вам недоступна. Обратитесь к оператору*
2010 | *Некорректная структура пакета*
3013 | *Недостаточно полномочий для выполнения операции*
3027 | *Операция с данным Id была использована ранее*
3037 | *Неверный код подтверждения*
3038 | *Ваш номер уже занят процессом оплаты, завершите оплату или подождите 5 минут*
3040 | *Превышено количество попыток ввода*
3068 | *Операция недоступна*
3069 | *Операция не найдена*
3077 | *Номер не принадлежит оператору*
4001 | *Неклассифицированная ошибка*
4007 | *Платёж запрещён*
4009 | *Технические проблемы на стороне мерчанта*
4010 | *Мерчант временно недоступен*
4013 | *Неверный формат номера*
5001 | *Сервис не найден*
5002 | *Проверка на валидацию не прошла*
5011 | *Операция не найдена*
5012 | *Не найдена дочерняя операция*


#### Возможные коды состояния HTTP:

- HTTP status code 201 Created
  - Ресурс был успешно создан в ответ на POST-запрос. Заголовок Location содержит URL, указывающий на только что созданный ресурс


- HTTP status code 400 - Bad Request
  - Неверный запрос. Может быть связано с разнообразными проблемами на стороне пользователя, такими как неверные JSON-данные в теле запроса, неправильные параметры действия, и т.д.


- HTTP status code 403 - Forbidden
  - У вас нет прав для пользования данным действием или ресурсом

- HTTP status code 404 - Not Found
  - Не удается найти данные согласно запросу


- HTTP status code 422 - Unprocessable Entity
  - Проверка данных завершилась неудачно. Подробные сообщения об ошибках смотрите в теле ответа.


- HTTP status code 500 - Internal server error
  - Внутренняя ошибка сервера. Возможная причина — ошибки в самой программе
