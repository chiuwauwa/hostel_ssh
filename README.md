# hostel_ssh
### Описание
Подключение к малине по ssh но не через консоль
### Вызывается окно, в котором:
- Информация о подключении
- Кнопки:
- Подключение к малинке
- Воспроизведение файла muter
- Остановка воспроизведения
- Воспроизведение файла Intro
- Пустая строчка
- Отключение от малинки
- Выключение малинки

- На кнопку закрытие окна привязана проверка наличия соединения, 
если оно есть, предложит выключить малинку
если нет, просто закроет программу
    
### Технологии
Python 3.7
библиотеки:
tkinter
paramiko
pyinstaller
### Запуск проекта 
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом hoslel.py выполните команду:
```
 pyinstaller --onefile --window --icon=\hostel.ico hostel.py
```
### Авторы
Ni_kiss а файл для ubuntu запилит pan_gus
