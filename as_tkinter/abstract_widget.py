#!/usb/bin/env python3

import tkinter as tk

import ttkbootstrap


class AbstractWidget:
    """Абстрактный компонент с общими методами для всех компонентов
    """
    def __init__(self, **kwargs):
        """Инициализация виджета, параметры в kwargs:

           # Common (label)
           text - текст
           justify - выравнивание LEFT, RIGHT, CENTER
           anchor - точка начала виджета компасом E, SW
           width - ширина
           height - высота
           bg - фон виджета red
           fg - цвет текста виджета green
           bd
           relief # RAISED, SUNKEN
           font - шрифт Arial 20 italic | ('Comic Sans MS', 20, 'bold', 'underline')
           padx - отступ по х
           pady - отступ по у
           cursor - курсор
           image - изображение PhotoImage(file='logo.png')
           underline - подчеркивание символа 1 (не робит)
           wraplength - перенос строки по ширине

           # Button
           activebackground - фон для активной кнопки
           state - состояние кнопки NORMAL, ACTIVE, DISABLED
           borderwidth - ширина рамки
           command - функция при нажатии

           # LabelFrame
           labelanchor - расположение текста на рамке по компасу SE
        """
        pass

    @classmethod
    def check_kwargs(self, **kwargs):
        """Преобразование параметров из строк в константы
           например, side='BOTTOM' => tk.BOTTOM
        """
        for key, value in kwargs.items():
            if key in (
                'justify', 'relief', 'sashrelief', 'state',
                'side', 'wrap', 'fill', 'anchor',
                'labelanchor', 'sticky', 'orient', 'arrow',
            ):
                kwargs[key] = getattr(tk, value.upper())
            if key in (
                'bootstyle',
            ):
                if isinstance(value, (list, tuple)):
                    kwargs[key] = [
                        getattr(tk, item.upper())
                        for item in value
                    ]
                else:
                    kwargs[key] = getattr(ttkbootstrap.constants, value.upper())
        return kwargs

    def pack(self, **kwargs):
        """Выводит виджет и возвращает экземпляр, параметры в kwargs:
           ['side'] = TOP # выводит виджет в нужную область (LEFT, BOTTOM)
           ['expand'] = 1 # заполняет пространство виджетом (False, 0)
           ['fill'] = 'X' # растянуть виджет (X, Y, BOTH)
           ['anchor'] = 'S' # позиционировать виджет по компасу (E, NE, SW)
        """
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        """Выводит виджет и возвращает экземпляр, параметры в kwargs:
           ['x'] = 30 # виджет в x координату
           ['y'] = 60 # виджет в y координату
           ['relx'] = 0.5 # виджет в позицию от ширины родительского контейнера (0-1)
           ['rely'] = 0.5 # виджет в позицию от высоты родительского контейнера (0-1)
           ['anchor'] = 'CENTER' # задает точку начала виджета (можно компасом SE)
           ['relwidth'] = 0.5 # задать ширину виджета (0-1)
           ['relheight'] = 0.5 # задать высоту виджета (0-1)
        """
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        """Выводит виджет и возвращает экземпляр, параметры в kwargs:
           ['row'] = 0 # виджет в 0 строку
           ['column'] = 0 # виджет в 0 ряд
           ['columnspan'] = 2 # объединяет в строке 2 столбца
           ['rowspan'] = 2 # объединяет в стобце 2 строки
           ['ipadx'] = 10 # отступ по x
           ['ipady'] = 10 # отступ по y
           ['padx'] = 10 # отступ по x
           ['pady'] = 10 # отступ по y
           Параметры padx и pady повзвозяют установить отступы по горизонтали и вертикали
           от границ ячейки грида до границ виджета,
           а ipadx и ipady - отступы по горизонтали и вертикали внутри виджета
           от границ виджета до его содержимого 
           ['sticky'] = SW # позиционирование элемента в ячейке по компасу
                        n: положение вверху по центру
                        e: положение в правой части контейнера по центру
                        s: положение внизу по центру
                        w: положение в левой части контейнера по центру
                        nw: положение в верхнем левом углу
                        ne: положение в верхнем правом углу
                        se: положение в нижнем правом углу
                        sw: положение в нижнем левом углу
                        ns: растяжение по вертикали
                        ew: растяжение по горизонтали
                        nsew: растяжение по горизонтали и вертикали
           # Настройка сетки
           root.rowconfigure(index=0, weight=1)
           root.columnconfigure(index=0, weight=1)
             weight: 
               weight=0 (Default): Не меняет размер (ширина виджетов);
               weight=1 занимаем столько сколько может
               weight=2 в два раза больше занимает чем 1
             minsize: Минимальная ширина в пикселях для колонки, а для строки по высоте
             pad: отступ в пикселях по ширине для колонки, а для строки по высоте
        """
        super().grid(**self.check_kwargs(**kwargs))
        return self

    @classmethod
    def bind(cls, **kwargs):
        """Привязывает функцию к виджету
           Использование, 
           def test_bind(event):
               print('test bind', event)
           Label(**{'text':'test-bind'}).bind(test_bind)
           root.bind('<Key>', test_bind) # проверка какая клавиша была нажата
           kwargs['sequence'] = <Button-1> строка описывающая действие пользователя
           kwargs['func'] = print функция, которая должна выполниться
        """
        cls.bind(**kwargs)


class StringVar(tk.StringVar):
    """Переменная, например, для Radiobutton
    """
    def set(self, value: str):
        """Установить значение переменной
           string_var.set('test')
           :param value: значение
        """
        super().set(value)

    def get(self):
        """Получить значение переменной
        """
        return super().get()


class BooleanVar(tk.BooleanVar):
    """Переменная, например, для Radiobutton
    """
    def set(self, value: int):
        """Установить значение переменной
           boolean_var.set(0)
           :param value: значение
        """
        super().set(value)

    def get(self):
        """Получить значение переменной
        """
        return super().get()


class IntVar(tk.IntVar):
    """Переменная, например, для Scale
    """
    def set(self, value: int):
        """Установить значение переменной
           boolean_var.set(0)
           :param value: значение
        """
        super().set(value)

    def get(self):
        """Получить значение переменной
        """
        return super().get()
