## Справочники:

1. Модель техники

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

2. Модель двигателя

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

3. Модель трансмиссии

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

4. Модель ведущего моста

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

5. Модель управляемого моста

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

6. Вид технического обслуживания

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

7. Сервисная компания

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

8. Узел отказа

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

9. Способ восстановления

| name_col | format  | info |
| -------- | ------- | ---- |
| name     | varchar | pk   |
| discribe | varchar |      |

## Документы (сущности)

10. Машина

| name_col                               | format  | info |
| -------------------------------------- | ------- | ---- |
| Зав. № машины                          | varchar | pk   |
| Модель техники                         | varchar | fk   |
| Модель двигателя                       | varchar | fk   |
| Зав № двигателя                        | varchar |      |
| Модель трансмиссии                     | varchar | fk   |
| Зав № трансмиссии                      | varchar |      |
| Модель ведущего моста                  | varchar | fk   |
| Зав № ведущего моста                   | varchar |      |
| Модель управляемого моста              | varchar | fk   |
| Зав № управляемого моста               | varchar |      |
| Договор поставки №, дата               | varchar |      |
| Дата отгрузки с завода                 | date    |      |
| Грузополучатель (конечный потребитель) | varchar |      |
| Адрес поставки (эксплуатации)          | varchar |      |
| Комплектация (доп. опции)              | varchar |      |
| Клиент                                 | varchar |      |
| Сервисная компания                     | varchar | fk   |

11. Техническое обслуживание

| name_col           | format  | info |
| ------------------ | ------- | ---- |
| id машины          | varchar | fk   |
| Вид ТО             | varchar | fk   |
| Дата проведения ТО | date    | fk   |
| Наработка, м/час   | число   |      |
| Номер заказ-наряда | varchar |      |
| Дата заказ-наряда  | date    |      |
| сервисная компания | varchar | fk   |

12. Рекламации

| name_col                    | format  | info |
| --------------------------- | ------- | ---- |
| id машины                   | varchar | fk   |
| Дата отказа                 | date    |      |
| Наработка, м/час            | число   |      |
| Узел отказа                 | текст   | fk   |
| Описание отказа             | varchar |      |
| Способ восстановления       | varchar | fk   |
| Используемые запасные части | текст   |      |
| Дата восстановления         | date    |      |
| Время простоя техники       | varchar |      |
| сервисная компания          | varchar | fk   |

## Описание бизнес процесса

1. Выпуск ноаого образца техники

- ввод данных о машине и ее агрегатах
- ввод данных о покупателе (кому отгружена)

2. Эксплуатация техники клиентом - не регистрируется

3. Если поломки нет, то в срок проводится ТО машины

- вносится запись о ТО

4. Если произошла поломка

- вносится запись в рекламацию

## Структура:

my_silant/
├── backend/
│ ├── config/ # settings.py, urls.py, wsgi.py
│ ├── apps/
│ │ ├── core/ # BaseModel, менеджеры, миксины
│ │ ├── references/ # Все справочники
│ │ ├── organizations/ # Организация (клиенты/сервисы)
│ │ ├── users/ # Профиль, роли, права
│ │ ├── machines/ # Машина
│ │ ├── maintenance/ # ТО
│ │ └── claims/ # Рекламации
│ └── manage.py
└── requirements.txt
