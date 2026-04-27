#!/usb/bin/env python3


import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk


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
           ['sticky'] = SW # позиционирование элемента в ячейке по компасу
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


class PhotoImage(tk.PhotoImage):

    def __init__(self, file, **kwargs):
        """Инициализация изображения
           :param file: путь к файлу
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(file=file, **kwargs)


class Window(tk.Tk):
    """Окно
    root = Window(**{
        'title': 'test', 'geometry': '300x300', 'resizable': (0, 0),
    })
    """
    methods = (
        'title',
        'geometry',
        'resizable',
    )
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs.get('title'):
            self.title(kwargs['title'])
        if kwargs.get('geometry'):
            self.geometry(kwargs['geometry'])
        if kwargs.get('resizable'):
            self.resizable(*kwargs['resizable']) # root.resizable(0, 0)


class TopLevel(tk.Toplevel):
    """Дополнительное окно
    new_window = TopLevel(root, **{
        'title': 'test', 'geometry': '300x300', 'resizable': (0, 0),
        'grab_set': True, # не дает взаимодействовать с родительским
    })
    """
    methods = (
        'title',
        'geometry',
        'resizable',
        'grab_set',
    )
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        if kwargs.get('title'):
            self.title(kwargs['title'])
        if kwargs.get('geometry'):
            self.geometry(kwargs['geometry'])
        if kwargs.get('resizable'):
            self.resizable(*kwargs['resizable']) # root.resizable(0, 0)
        if kwargs.get('grab_set'):
            self.grab_set() # не дает взаимодействовать с родительским


class Menu(tk.Menu, AbstractWidget):
    """Меню в шапке, либо контекстное меню
    add_command(options): добавляет элемент меню через параметр options
    add_cascade(options): добавляет элемент меню, который представляет подменю
    add_separator(): добавляет линию-разграничитель
    add_radiobutton(options): добавляет в меню переключатель
    add_checkbutton(options): добавляет в меню флажок

    tearoff = 0
    main_menu = Menu(root, **{
        #'tearoff': tearoff, # убрать разделитель
    })
    # Верхний уровень
    root.config(menu=main_menu)
    # На маке не будет работать добавление в верхний уровень (только add_cascade меню)
    main_menu.add_command(label='Help')
    # Подуровень меню
    sub_menu = Menu(main_menu, **{'tearoff': tearoff})
    main_menu.add_cascade(label='File', menu=sub_menu)
    sub_menu.add_command(label='Open')
    sub_menu.add_separator() # разделитель
    sub_menu.add_command(label='Exit', command=quit)
    # Под-подуровень меню
    third_menu = Menu(sub_menu, **{'tearoff': tearoff})
    sub_menu.add_cascade(label='New', menu=third_menu)
    third_menu.add_command(
        label='add button',
        command=new_label,
    )

    # Контекстное меню
    def popup(event):
        print('x=%s, y=%s' % (event.x, event.y))
        context_menu.post(event.x_root, event.y_root)
    context_menu = Menu(**{'tearoff': 0})
    context_menu.add_command(label='New label')
    root.bind('<Button-2>', popup)
    """
    def __init__(self, parent=None, **kwargs):
        """Инициализация
           :param parent: родительский элемент
                          None, если контекстное меню
        """
        super().__init__(parent, **self.check_kwargs(**kwargs))


class Messagebox:
    """Модальное окно
    Messagebox.showinfo(**{'title': 'Info', 'message': 'Help text'})
    Messagebox.showwarning(**{'title': 'Warn', 'message': 'Warn text'})
    Messagebox.showerror(**{'title': 'Error', 'message': 'Error text'})
    ask = Messagebox.askquestion(**{'title': 'Add', 'message': 'Add action?'})
    if ask == 'yes':
        print('YES')
    ask = Messagebox.askokcancel(**{'title': 'Add', 'message': 'Add action?'})
    if ask:
        print('OK')
    ask = Messagebox.askretrycancel(**{'title': 'Add', 'message': 'Add action?'})
    if ask:
        print('OK')
    ask = Messagebox.askyesno(**{'title': 'Add', 'message': 'Add action?'})
    if ask:
        print('OK')
    ask = Messagebox.askyesnocancel(**{'title': 'Add', 'message': 'Add action?'})
    if ask:
        print('OK')
    """
    @staticmethod
    def showinfo(**kwargs):
        """Окно с информацией"""
        return tkinter.messagebox.showinfo(**kwargs)

    @staticmethod
    def showwarning(**kwargs):
        """Окно с предупреждением"""
        return tkinter.messagebox.showwarning(**kwargs)

    @staticmethod
    def showerror(**kwargs):
        """Окно с ошибкой"""
        return tkinter.messagebox.showerror(**kwargs)

    @staticmethod
    def askquestion(**kwargs):
        """Окно с вопросом"""
        return tkinter.messagebox.askquestion(**kwargs)

    @staticmethod
    def askokcancel(**kwargs):
        """Окно с вопросом"""
        return tkinter.messagebox.askokcancel(**kwargs)

    @staticmethod
    def askretrycancel(**kwargs):
        """Окно с вопросом о повторе"""
        return tkinter.messagebox.askretrycancel(**kwargs)

    @staticmethod
    def askyesno(**kwargs):
        """Окно с вопросом"""
        return tkinter.messagebox.askyesno(**kwargs)

    @staticmethod
    def askyesnocancel(**kwargs):
        """Окно с вопросом"""
        return tkinter.messagebox.askyesnocancel(**kwargs)


class Filedialog:
    """Окна с проводником для взаимодействия с файлами
    file_name = Filedialog.askopenfilename(**{'filetypes': (
        ('txt files', '*.txt'),
        ('html files', '*.html'),
    )})
    print(file_name)
    file_name = Filedialog.asksavefilename(**{'filetypes': (
        ('txt files', '*.txt'),
        ('html files', '*.html'),
    )})
    print(file_name)
    """
    @staticmethod
    def askopenfilename(**kwargs):
        """Диалог открытия файла"""
        return tkinter.filedialog.askopenfilename(**kwargs)

    @staticmethod
    def asksaveasfilename(**kwargs):
        """Диалог сохранения файла"""
        return tkinter.filedialog.asksaveasfilename(**kwargs)


class Canvas(tk.Canvas, AbstractWidget):
    """Холст для рисования
    canvas = Canvas(root, **{'width': 500, 'height': 500, 'bg': 'black'}).pack()
    canvas.create_rectangle(**{
        'x1': 20, 'y1': 20, 'x2': 70, 'y2': 70,
        'fill': 'lime', 'outline': 'white', 'width': 3,
    })
    canvas.create_oval(**{
        'x1': 80, 'y1': 20, 'x2': 130, 'y2': 70,
        'fill': 'lime', 'outline': 'white', 'width': 3,
    })
    canvas.create_polygon(*[
        160, 20, 135, 70, 185, 70,
    ], **{
        'fill': 'lime', 'outline': 'white', 'width': 3,
    })
    canvas.create_line(*[
        200, 100, 300, 300,
    ], **{
        'fill': 'lime', 'width': 3, 'arrow': 'last', 'arrowshape': '10 20 10',
        'activefill': 'white', 'dash': (15, 10),
    })
    canvas.create_text(**{
        'x1': 120, 'y1': 200, 'text': 'Проверка\nвывода текста\nна canvas',
        'font': 'Arial 15 bold', 'fill': 'lime', 'justify': 'center',
    })
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self

    def create_rectangle(self, **kwargs):
        """Нарисовать прямоугольник"""
        x1, y1 = kwargs.pop('x1'), kwargs.pop('y1')
        x2, y2 = kwargs.pop('x2'), kwargs.pop('y2')
        super().create_rectangle(x1, y1, x2, y2, **kwargs)

    def create_oval(self, **kwargs):
        """Нарисовать овал"""
        x1, y1 = kwargs.pop('x1'), kwargs.pop('y1')
        x2, y2 = kwargs.pop('x2'), kwargs.pop('y2')
        super().create_oval(x1, y1, x2, y2, **kwargs)

    def create_polygon(self, *args, **kwargs):
        """Нарисовать полигон"""
        super().create_polygon(*args, **kwargs)

    def create_line(self, *args, **kwargs):
        """Нарисовать линию"""
        super().create_line(*args, **kwargs)

    def create_text(self, *args, **kwargs):
        """Вывести текст"""
        x1, y1 = kwargs.pop('x1'), kwargs.pop('y1')
        super().create_text(x1, y1, **kwargs)


class PanedWindow(tk.PanedWindow, AbstractWidget):
    """Окно внутри другого окна с возможностью изменения размеров
    screen = PanedWindow(root).pack(fill='BOTH', expand=1)
    label = Label(screen, text='Left side')
    screen.add(label)
    # Вертикальная панелька
    screen2 = PanedWindow(
        screen,
        orient='VERTICAL', # виджеты идут вертикально
        showhandle=True, # показывает ползунок для изменения размеров
        handlesize=20, # размер ползунка для изменения размеров
        sashpad=15, # отступы от ползунка масштабирования
        sashrelief='RAISED', # рамка ползунка масштабирования
        sashwidth=15, # ширина границы ползунка масштабирования
    )
    screen.add(screen2)
    entry = Entry(screen2)
    screen2.add(entry)
    button = Button(screen2, text='button')
    screen2.add(button)
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Frame(tk.Frame, AbstractWidget):
    """Фрейм для размещения в окне, а в него уже размещаются виджеты
    frame = Frame(root).pack(**{
        'side': 'BOTTOM',
    })
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class LabelFrame(tk.LabelFrame, AbstractWidget):
    """Фрейм для размещения с рамокй и заголовком в окне,
       а в него уже размещаются виджеты
    frame = LabelFrame(root, **{
        'text': 'Фрейм', 'labelanchor': 'SE',
    }).pack(**{
        'side': 'BOTTOM',
    })
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Label(tk.Label, AbstractWidget):
    """Метка
    label = Label(root, **{
        'text': 'ДРАТУЙ test\ntest2', 'fg': 'lime', 'bg': 'black',
        'font': ('Arial', 20), #'Arial 20 bold underline',
        #'width': 10, 'height': 10, 'bd': 10,
        #'padx': 10, 'pady': 10,
        'cursor': 'man',
        #'image': PhotoImage(file='/Users/jocker/Documents/223/design/call_button.png'),
        #'justify': 'RIGHT', # работает в рамках текста, не по ширине label
        #'anchor': 'e', # якорь компасом
        #'relief': 'SUNKEN', # работает с bd
        'underline': 0, # подчеркивает символ по индексу для горячих клавиш (не робит)
        'wraplength': 50, # перенос строки по ширине
    }).pack(side='TOP', expand=False)
    Можно изменять текст через
    label['text'] = '123'
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class StandardButton(tk.Button, AbstractWidget):
    """Стандартная кнопка
    button = StandardButton(root, **{
        'text': 'Жмакай', 'fg': 'lime', 'bg': 'black',
        'font': ('Arial', 20),
        'activebackground': 'red',
        #'state': 'DISABLED',
        'borderwidth': 10,
        'command': print, # функция
    }).pack(side='RIGHT', expand=False)
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Button(ttk.Button, AbstractWidget):
    """Кнопка
    button = Button(root, **{
        'text': 'Жмакай',
        'command': print, # функция
    }).pack()
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Radiobutton(tk.Radiobutton, AbstractWidget):
    """Кнопка radio button
    var = StringVar()
    var.set('blue')
    def select_color():
        label['bg'] = var.get()
    radio_button = Radiobutton(root, **{
        'text': 'Blue',
        'font': ('Arial', 20),
        'activebackground': 'orange', # цвет фона в активном состоянии
        'activeforeground': 'green', # цвет текста в активном состоянии
        'selectcolor': 'pink', # цвет кружочка в активном состоянии
        'fg': 'blue',
        'value': 'blue', # значение
        'variable': var, # переменная
        'command': select_color, # функция
    }).pack()
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Checkbutton(tk.Checkbutton, AbstractWidget):
    """Флажок checkbox
       У каждого флажка должна быть своя переменная!
    var = BooleanVar()
    var.set(0)
    def select_color():
        label['bg'] = var.get()
    check_button = Checkbutton(root, **{
        'text': 'Blue',
        'font': ('Arial', 20),
        'activebackground': 'orange', # цвет фона в активном состоянии
        'activeforeground': 'green', # цвет текста в активном состоянии
        'selectcolor': 'pink', # цвет кружочка в активном состоянии
        'fg': 'blue',
        'onvalue': 1, # значение при активном
        'offvalue': 0, # значение при неактивном
        'variable': var, # переменная
        'command': select_color, # функция
    }).pack()
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class OptionMenu(tk.OptionMenu, AbstractWidget):
    """Выпадющий список select
    var = StringVar()
    fonts_list = ['Arial', 'Comic Sans MS', 'Times New Roman']
    menu = OptionMenu(root, *fonts_list, **{
        'variable': var,
        'command': print,
    }).pack()
    menu.config(width=90, font='Arial 20')
    """
    def __init__(self, parent, *args, **kwargs):
       variable = kwargs.pop('variable', StringVar())
       super().__init__(parent, variable, *args, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Combobox(ttk.Combobox, AbstractWidget):
    """Выпадющий список select
    combo = Combobox(root, **{
        'font': 'Arial 15 bold',
        'values': ['january', 'february', 'march', 'april'],
    }).pack(fill='X')
    combo.current(1) # выбираем по умолчанию
    def combo_select(event):
        print(event, combo.get())
    combo.bind('<<ComboboxSelected>>', combo_select)
    """
    def __init__(self, parent, *args, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Scale(tk.Scale, AbstractWidget):
    """Шкала (ползунок)
    scale = Scale(root, **{
        'from_': 0,
        'to': 100,
        'orient': 'HORIZONTAL',
        'troughcolor': 'pink', # фон шкалы
        'tickinterval': 25, # вывод шага (пояснения к значениям)
        'sliderlength': 30, # ширина ползунка
        'showvalue': True, # вывод текущего значения над шкалой
    }).pack()
    """
    def __init__(self, parent, *args, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self

    def set(self, value: int):
        """Установить значение на шкале
           int_var.set(45)
           :param value: значение
        """
        super().set(value)

    def get(self):
        """Получить значение на шкале
        """
        return super().get()


class LabeledScale(ttk.LabeledScale, AbstractWidget):
    """Шкала (ползунок)
    scale = LabeledScale(root, **{
        'from_': 0,
        'to': 100,
    }).pack()
    print(scale.value)
    scale.value = 33
    print(scale.value)
    """
    def __init__(self, parent, *args, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Spinbox(tk.Spinbox, AbstractWidget):
    """Выбор значения через стрелки без выпадающего списка
    spin_box = Spinbox(root, **{
        'from_': 0,
        'to': 100,
        #'values': ('python', 'java', 'c++', 'c#'), # вместо from_ и to
        'increment': 2, # шаг
        'justify': 'CENTER', # выравнивание значения в поле ввода
        'repeatdelay': 10, # задержка изменения значения в мс при зажатой кнопке
        'repeatinterval': 20, # время изменения значения в мс при зажатой кнопке
    }).pack()
    """
    def __init__(self, parent, *args, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Entry(tk.Entry, AbstractWidget):
    """Ввод текста
    entry = Entry(root, **{
        'font': ('Arial', 20),
    }).pack(side='BOTTOM', expand=True)
    entry.insert(0, 'hello')
    entry.insert(5, 'world')
    entry.delete(0, 5)
    print(entry.get())
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self

    def insert(self, start_index: int = 0, text: str = ''):
        """Вставка текста
           :param start_index: начальный индекс
           :param text: текст
        """
        super().insert(start_index, text)

    def delete(self, start_index: int = 0, end_index: int = tk.END):
        """Удаление текста
           :param start_index: начальный индекс
           :param end_index: конечный индекс
        """
        super().delete(start_index, end_index)

    def get(self):
        """Получение текста
        """
        return super().get()


class Text(tk.Text, AbstractWidget):
    """Ввод многострочного текста
    text = Text(root, **{
        'font': ('Arial', 20),
        'highlightthickness': 10, # рамка вокруг поля
        'highlightcolor': 'lime', # цвет рамки вокруг поля при фокусе ввода
        'highlightbackground': 'red', # цвет рамки вокруг поля без фокуса ввода
        'insertbackground': 'green', # цвет курсора
        'insertofftime': 100, # время неактивного курсора (неактивен 100мс - мигает)
        'insertontime': 1000, # мигание активного курсора
        'insertwidth': 10, # ширина курсора ввода
        'selectbackground': 'orange', # цвет выделенного текста
        'spacing1': 15, # вертикальный отступ между абзацами (отступ свехру)
        'spacing2': 15, # вертикальный отступ между строками
        'spacing3': 15, # вертикальный отступ между абзацами (отступ снизу)
        'tabs': 10, # размер табов
        'wrap': 'WORD', # перенос по словам
    }).pack(side='BOTTOM', expand=True)
    text.insert(1.0, 'hello') # 1.0 => line 1, char 0
    text.insert(1.5, 'world') # 1.5 => line 1, char 5
    text.delete(1.0, 1.5) # 1.0 => line 1, char 0, 1.5 => line 1, char 5
    print(text.get())
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self

    def insert(self, start_index: float = 0.0, text: str = ''):
        """Вставка текста
           text.insert(1.0, 'hello') # 1.0 => line 1, char 0
           :param start_index: начальный индекс
           :param text: текст
        """
        super().insert(start_index, text)

    def append(self, text: str = ''):
        """Вставка текста в конец
           text.append('hello')
           :param text: текст
        """
        self.insert(start_index=tk.END, text=text)

    def delete(self, start_index: float = 0.0, end_index: float = tk.END):
        """Удаление текста
           text.delete(1.0, 1.5) # 1.0 => line 1, char 0, 1.5 => line 1, char 5
           :param start_index: начальный индекс
           :param end_index: конечный индекс
        """
        super().delete(start_index, end_index)

    def get(self, start_index: float = 0.0, end_index: float = tk.END):
        """Получение текста
           print(text.get(1.0, 1.3)) # 1.0 => line 1, char 0, 1.3 => line1, char 3
           :param start_index: начальный индекс
           :param end_index: конечный индекс
        """
        return super().get(start_index, end_index)


class Scrollbar(tk.Scrollbar, AbstractWidget):
    """Ползунок прокрутки
    text = Text(root).pack(side='LEFT')
    scroll = Scrollbar(root, **{
        'command': text.yview, # text - это виджет, который скролим (Text)
    }).pack(fill='Y', side='LEFT')
    text.config(yscrollcommand=scroll.set)
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Listbox(tk.Listbox, AbstractWidget):
    """Список элементов
    list_box = Listbox(root, **{
        'font': ('Arial', 20),
    }).pack()
    scroll = Scrollbar(root, **{
        'command': list_box.yview, # list_box - это виджет, который скролим
    }).pack(fill='Y', side='LEFT')
    list_box.config(yscrollcommand=scroll.set)
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self

    def get(self, index: int = 0):
        """Получить элемент
        """
        return super().get(index)

    def insert(self, index: int = 0, text: str = ''):
        """Вставка элемента
           :param index: индекс
           :param text: текст
        """
        super().insert(index, text)

    def append(self, text: str = ''):
        """Вставка элемента в конец списка
           :param text: текст
        """
        self.insert(index=tk.END, text=text)

    def delete(self, start_index: int = 0, end_index: int = tk.END):
        """Удаление элементов
           list_box.delete(list_box.curselection())
           :param start_index: начальный индекс
           :param end_index: конечный индекс
        """
        super().delete(start_index, end_index)

    def curselection(self) -> list:
        """Получение выбранных элементов
        """
        return super().curselection()

    def size(self):
        """Кол-во элементов
        """
        super().size()


class Notebook(ttk.Notebook, AbstractWidget):
    """Вкладки (tabs)
    tabs = Notebook(root).pack(expand=1, fill='BOTH')
    tab1 = Frame(tabs)
    tab2 = Frame(tabs)
    tabs.add(tab1, text='first')
    tabs.add(tab2, text='second')
    label1 = Label(tab1, text='first tab').grid(column=0, row=0)
    label2 = Label(tab2, text='second tab').grid(column=0, row=0)
    def add_tab():
        tab = Frame(tabs)
        tabs.add(tab, text='new')
    Button(root, **{'text': 'add', 'command': add_tab}).pack()
    """
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


class Progressbar(ttk.Progressbar, AbstractWidget):
    """Шкала процента выполнения работы
    progress_bar = Progressbar(root, **{
        'maximum': 100,
        'value': 0,
        'length': 150,
        'mode': 'determinate', # indeterminate
    }).pack()
    #progress_bar.start()
    progress_bar.step(amount=50)
    progress_bar.stop()
    """
    def __init__(self, parent, *args, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self

    def start(self, interval: int = 10):
        """Запуск заполнения шкалы
           :param interval: время через которое увеличивается заполнение
        """
        super().start(interval=interval)

    def step(self, amount: int = 2):
        """Единоразовое увеличение шкалы
           :param amount: число на которое увеличивается заполнение
        """
        super().step(amount=amount)

    def stop(self):
        """Останавливет заполнение шкалы (будет пустой без заполнения)
        """
        super().stop()


class Separator(ttk.Separator, AbstractWidget):
    """Разделитель
    separator = Separator(root, **{
        'orient': 'HORIZONTAL',
    }).pack(fill='X')
    separator = Separator(root, **{
        'orient': 'VERTICAL',
    }).pack(fill='Y', expand=1)
    # Изменить стиль
    s = ttk.Style()
    s.configure('TSeparator', background='lime', border=100)
    """
    def __init__(self, parent, *args, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self, **kwargs):
        super().pack(**self.check_kwargs(**kwargs))
        return self

    def place(self, **kwargs):
        super().place(**self.check_kwargs(**kwargs))
        return self

    def grid(self, **kwargs):
        super().grid(**self.check_kwargs(**kwargs))
        return self


if __name__ == '__main__':
    root = Window(**{
        'title': 'test', 'geometry': '800x800', 'resizable': (0, 0),
    })

    # Вывод тем операционной системы
    style = ttk.Style()
    print('themes: %s, current theme: %s' % (style.theme_names(), style.theme_use()))
    style.theme_use('clam') # Установить используемую тему

    separator = Separator(root, **{
        'orient': 'VERTICAL',
    }).pack(fill='Y', expand=1)
    # Изменить стиль
    style.configure('TSeparator', background='lime', border=100)

    root.mainloop()
