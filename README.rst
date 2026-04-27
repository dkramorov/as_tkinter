Описание
-----------
Менеджер для работы с Tkinter

Установка пакетом
-----------
Для локальной разработки::
    pip install -e packages/as_tkinter
Для обычной установки через requirements.txt::
    as_tkinter @ git+https://github.com/dkramorov/as_tkinter.git

Импорт
-----------
Проверка::
    from as_tkinter.tkinter_manager import Window
    root = Window(**{
        'title': 'test', 'geometry': '800x800', 'resizable': (0, 0),
    })
    root.mainloop()


Удаление
-----------
Удалить пакет::
    pip uninstall as_tkinter

Для создания пакета
https://docs.python.org/3.10/distutils/introduction.html#distutils-simple-example
https://docs.python.org/3.10/distutils/sourcedist.html
::
    python setup.py sdist




