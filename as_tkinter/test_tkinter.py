#!/usb/bin/env python3


from as_tkinter.tkinter_manager import *
from tkinter import ttk


if __name__ == '__main__':
    root = Window(**{
        'title': 'test', 'geometry': '1200x900', 'resizable': (0, 0),
    })

    style = ttk.Style()

    def test_bind(event):
        print('test bind', event)
        list_box_selection = list_box.curselection()
        if list_box_selection:
            print('list_box delete %s' % list_box_selection)
            list_box.delete(
                start_index=list_box_selection[0],
                end_index=list_box_selection[0],
            )
        #new_window = TopLevel(root, **{
        #    'title': 'test', 'geometry': '300x300', 'resizable': (0, 0),
        #    'grab_set': True,
        #})

    root.bind('<Key>', test_bind) # проверка какая клавиша была нажата

    frame = Frame(root).pack(**{
        'side': 'BOTTOM',
    })
    label1 = Label(frame, **{
        'text': 'label1', 'bg': 'red'
    }).pack(**{'side': 'LEFT', 'pady': 5, 'padx': 5})
    label2 = Label(frame, **{
        'text': 'label2', 'bg': 'green'
    }).pack(**{'side': 'LEFT', 'pady': 5, 'padx': 5})

    frame = LabelFrame(root, **{'text': 'Фрейм', 'labelanchor': 'SE'}).pack(**{
        'side': 'BOTTOM', 'fill': 'X', 'padx': 5,
    })
    label1 = Label(frame, **{
        'text': 'label1', 'bg': 'red'
    }).pack(**{'side': 'LEFT', 'pady': 5, 'padx': 5})
    label2 = Label(frame, **{
        'text': 'label2', 'bg': 'green'
    }).pack(**{'side': 'LEFT', 'pady': 5, 'padx': 5})

    frame = Frame(root).pack(**{
        'padx': 5, 'pady': 5,
    })
    label1 = Label(frame, **{
        'text': 'label1', 'bg': 'red'
    }).grid(**{'row': 0, 'column': 0})
    label2 = Label(frame, **{
        'text': 'label2', 'bg': 'green'
    }).grid(**{'row': 0, 'column': 1})
    label3 = Label(frame, **{
        'text': 'label3', 'bg': 'yellow'
    }).grid(**{'row': 1, 'column': 1})

    def new_label():
        label = Label(root, **{
            'text': 'ДРАТУЙ test\ntest2', 'fg': 'lime', 'bg': 'black',
            'cursor': 'man',
        }).pack(fill='X')
        # entry должна быть создана до вызова
        label['text'] = entry.get()

    button = StandardButton(root, **{
        'text': 'Жмакай', 'fg': 'lime', 'bg': 'black',
        'font': ('Arial', 20),
        'activebackground': 'red',
        #'state': 'DISABLED',
        'borderwidth': 10,
        'command': new_label, # функция
    }).pack(side='RIGHT')
    button.bind(**{'sequence': '<Button-1>', 'func': test_bind})

    entry = Entry(root, **{
        'font': ('Arial', 20),
    }).pack(side='BOTTOM', expand=True, fill='X', anchor='E')
    entry.insert(0, 'hello')
    entry.insert(5, 'world')
    entry.delete(0, 5)
    print(entry.get())

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
        #'spacing1': 15, # вертикальный отступ между абзацами (отступ свехру)
        #'spacing2': 15, # вертикальный отступ между строками
        'spacing3': 15, # вертикальный отступ между абзацами (отступ снизу)
        'wrap': 'WORD',
        'width': 10,
        'height': 10,
    }).pack(side='LEFT')
    text.insert(1.0, 'hello') # 1.0 => line 1, char 0
    text.insert(1.5, 'world') # 1.5 => line 1, char 5
    text.delete(1.0, 1.5) # 1.0 => line 1, char 0, 1.5 => line 1, char 5
    print(text.get(1.0, 1.3)) # 1.0 => line 1, char 0, 1.3 => line1, char 3
    print(text.get(1.2))

    scroll = Scrollbar(root, **{
        'command': text.yview, # text - это виджет, который скролим (Text)
    }).pack(fill='Y', side='LEFT')
    text.config(yscrollcommand=scroll.set)

    select_color_var = StringVar()
    select_color_var.set('blue')
    def select_color():
        text['bg'] = select_color_var.get()
        #list_box.insert(text=select_color_var.get())
        list_box.append(text=select_color_var.get())

    radio_button = Radiobutton(root, **{
        'text': 'Blue', 'fg': 'blue',
        'font': ('Arial', 20),
        'value': 'blue',
        'variable': select_color_var, # переменная
        'command': select_color,
    }).pack()
    radio_button = Radiobutton(root, **{
        'text': 'Red', 'fg': 'red',
        'font': ('Arial', 20),
        'value': 'red',
        'variable': select_color_var, # переменная
        'command': select_color,
    }).pack()

    var1 = BooleanVar()
    var1.set(0)
    def select_color1():
        text.append(text='\ncheckbutton1 => %s' % var1.get())
    check_button = Checkbutton(root, **{
        'text': 'Blue',
        'font': ('Arial', 20),
        'activebackground': 'orange', # цвет фона в активном состоянии
        'activeforeground': 'green', # цвет текста в активном состоянии
        'selectcolor': 'pink', # цвет кружочка в активном состоянии
        'fg': 'blue',
        'onvalue': 1, # значение при активном
        'offvalue': 0, # значение при неактивном
        'variable': var1, # переменная
        'command': select_color1, # функция
    }).pack()
    var2 = BooleanVar()
    var2.set(0)
    def select_color2():
        text.append(text='\ncheckbutton2 => %s' % var2.get())
    check_button = Checkbutton(root, **{
        'text': 'Pink',
        'font': ('Arial', 20),
        'activebackground': 'orange', # цвет фона в активном состоянии
        'activeforeground': 'green', # цвет текста в активном состоянии
        'selectcolor': 'pink', # цвет кружочка в активном состоянии
        'fg': 'pink',
        'onvalue': 1, # значение при активном
        'offvalue': 0, # значение при неактивном
        'variable': var2, # переменная
        'command': select_color2, # функция
    }).pack()

    list_box = Listbox(root, **{
        'font': ('Arial', 20),
        'width': 12,
    }).pack(side='LEFT')
    scroll = Scrollbar(root, **{
        'command': list_box.yview, # list_box - это виджет, который скролим
    }).pack(fill='Y', side='LEFT')
    list_box.config(yscrollcommand=scroll.set)
    for item in ('banana', 'apple', 'pear', 'grape', 'orange', 'mango'):
        list_box.insert(index=0, text=item)
    print('before=%s, start_element=%s' % (list_box.size(), list_box.get(0)))
    #list_box.delete(list_box.curselection())
    #print('after=%s, start_element=%s' % (list_box.size(), list_box.get(0)))

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
    button = StandardButton(screen2, text='button')
    screen2.add(button)

    var = StringVar()
    fonts_list = ['Arial', 'Comic Sans MS', 'Times New Roman']
    menu = OptionMenu(root, *fonts_list, **{
        'variable': var,
        'command': print,
    }).pack()
    menu.config(width=90, font='Arial 20')

    scale = Scale(root, **{
        'from_': 0,
        'to': 100,
        'orient': 'HORIZONTAL',
        'troughcolor': 'pink', # фон шкалы
        'tickinterval': 25, # вывод шага (пояснения к значениям)
        'sliderlength': 30, # ширина ползунка
        'showvalue': True, # вывод текущего значения над шкалой
    }).pack()
    print(scale.get())
    scale.set(33)
    print(scale.get())

    spin_box = Spinbox(root, **{
        'from_': 0,
        'to': 100,
        'values': ('python', 'java', 'c++', 'c#'), # вместо from_ и to
        'increment': 2, # шаг
        'justify': 'CENTER', # выравнивание значения в поле ввода
        #'repeatdelay': 10, # задержка изменения значения в мс при зажатой кнопке
        #'repeatinterval': 20, # время изменения значения в мс при зажатой кнопке
    }).pack()


    tearoff = 0
    main_menu = Menu(root, **{
        #'tearoff': tearoff, # убрать разделитель
    })
    # Верхний уровень
    root.config(menu=main_menu)
    # Подуровень меню
    sub_menu = Menu(main_menu, **{'tearoff': tearoff})
    main_menu.add_cascade(label='File', menu=sub_menu)
    sub_menu.add_command(label='Open')
    sub_menu.add_separator() # разделитель
    sub_menu.add_command(label='Exit', command=quit)
    # Под-подуровень меню
    third_menu = Menu(sub_menu, **{'tearoff': tearoff})
    sub_menu.add_cascade(label='New', menu=third_menu)

    def open_file():
        file_name = Filedialog.askopenfilename(**{'filetypes': (
            ('txt files', '*.txt'),
            ('html files', '*.html'),
        )})
        print(file_name)
    third_menu.add_command(
        label='Open file',
        command=open_file,
    )

    def save_file():
        file_name = Filedialog.asksaveasfilename(**{'filetypes': (
            ('txt files', '*.txt'),
            ('html files', '*.html'),
        )})
        print(file_name)
    third_menu.add_command(
        label='Save file',
        command=save_file,
    )

    def popup(event):
        print('x=%s, y=%s' % (event.x, event.y))
        context_menu.post(event.x_root, event.y_root)
    context_menu = Menu(**{'tearoff': 0})
    context_menu.add_command(label='New label')
    root.bind('<Button-3>', popup)

    #Messagebox.showinfo(**{'title': 'Info', 'message': 'Help text'})
    #Messagebox.showwarning(**{'title': 'Warn', 'message': 'Warn text'})
    #Messagebox.showerror(**{'title': 'Error', 'message': 'Error text'})
    #ask = Messagebox.askquestion(**{'title': 'Add', 'message': 'Add action?'})
    #if ask == 'yes':
    #    print('YES')
    #ask = Messagebox.askokcancel(**{'title': 'Add', 'message': 'Add action?'})
    #if ask:
    #    print('OK')
    #ask = Messagebox.askretrycancel(**{'title': 'Add', 'message': 'Add action?'})
    #if ask:
    #    print('OK')
    #ask = Messagebox.askyesno(**{'title': 'Add', 'message': 'Add action?'})
    #if ask:
    #    print('OK')
    #ask = Messagebox.askyesnocancel(**{'title': 'Add', 'message': 'Add action?'})
    #if ask:
    #    print('OK')

    """
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

    # TTK:

    button = Button(root, **{
        'text': 'Жмакай',
        'command': print, # функция
    }).pack()

    scale = LabeledScale(root, **{
        'from_': 0,
        'to': 100,
    }).pack()
    print(scale.value)
    scale.value = 33
    print(scale.value)

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

    combo = Combobox(root, **{
        'font': 'Arial 15 bold',
        'values': ['january', 'february', 'march', 'april'],
    }).pack(fill='X')
    combo.current(1) # выбираем по умолчанию
    def combo_select(event):
        print(event, combo.get())
    combo.bind('<<ComboboxSelected>>', combo_select)

    progress_bar = Progressbar(root, **{
        'maximum': 100,
        'value': 0,
        'length': 150,
        'mode': 'determinate', # indeterminate
    }).pack()
    #progress_bar.start()
    progress_bar.step(amount=50)
    progress_bar.stop()

    separator = Separator(root, **{
        'orient': 'HORIZONTAL',
    }).pack(fill='X')
    separator = Separator(root, **{
        'orient': 'VERTICAL',
    }).pack(fill='Y', expand=1)

    root.mainloop()