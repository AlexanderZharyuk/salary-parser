# SALARY PARSER

Скрипты по получению информации зарплат на биржах труда.

Анализ берется с сайтов: [HeadHunter](https://hh.ru/) и [SuperJob](https://www.superjob.ru/).


## Предустановка
1. Установите необходимые библиотеки:
Для этого используйте команду:
```shell
pip install -r requirements.txt
```
2. Настройте `.env` - файл:
Внутри этого файла должна быть переменная с вашим секретным ключом от API SuperJob:
```
SUPERJOB_SECRET_KEY=<YOUR-SECRET-KEY>
```

## Начало работы
Если вы хотите вывести получить данные по двум сайтам сразу, используйте команду:
```shell
python3 main.py
```
Данный скрипт начнет собирать информацию по сайтам по очереди и в конце выдаст таблицу подобного типа:

![Снимок экрана 2022-07-13 в 17 11 55](https://user-images.githubusercontent.com/103115934/178754677-2d17d496-2f11-4b73-84b8-545e01b036c0.png)

Во время работы скрипта вам будет виден прогресс работы, чтобы вы понимали, что скрипт все еще исполняется и на каком он этапе:

![Снимок экрана 2022-07-13 в 17 14 08](https://user-images.githubusercontent.com/103115934/178755205-6a76f432-055a-4464-a911-e83a2b8da245.png)

Если вам интересна таблица только по конкретной бирже используйте следующие команды:

Для **HH**:
```shell
python3 hh.py
```

Для **SuperJob**:
```shell
python3 superjob.py
```

На данном этапе скрипт ищет информацию только по Москве.

## Создано при помощи
* [Devman](https://dvmn.org/) - Обучающая платформа
* [HH](https://hh.ru/) - Сайт с вакансиями
* [SuperJob](https://www.superjob.ru/) - Сайт с вакансиями

## Автор
[Alexander Zharyuk](https://github.com/AlexanderZharyuk/)

## Фича на ближайший апдейт
- [ ] Добавить конфиг, в котором:
1. Юзер сможет выбирать id города, без исправления кода
2. Юзер может использовать собственные ключевые слова для поиска

