Инструкция по запуску:
1. Запустите компилятор в корне папки - RandomBook-main
2. Откройте консоль в корне папки
3. Введите следующие команды по очереди
   3.1. python -m venv .venv
   3.2. .venv\scripts\activate
   3.3. pip install -r requirements.txt
   3.4. alembic upgrade head
4. После успешной загрузки миграций, можно запускать приложение, введите следующую команду для запуска серверной части на локальном хосте:
   4.1. uvicorn app.main:app --reload
6. Запустите клиентскую часть на 5500 порту, можно использовать расширение LiveServer для Visual Studio Code, после загрузки расширения, в правом нижнем углу нажать на Go Live, открыть браузер и перейти на 127.0.0.1:5500/templates/index.html
   !!!Обязательно проверьте создался ли файл books.db и добавились ли книги в базу данных - на пункте 3.4.!!!
   Без этого, приложение будет не рабочим
   
