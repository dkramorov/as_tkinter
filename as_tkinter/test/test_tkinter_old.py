#!/usb/bin/env python3


import tkinter as tk
import tkinter.messagebox as msg


class AbstractWidget:
    """Абстрактный компонент с общими методами для всех компонентов
    """
    @classmethod
    def check_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key in ('justify', 'relief', 'state'):
                kwargs[key] = getattr(tk, value)
        return kwargs


class PhotoImage(tk.PhotoImage):

    def __init__(self, file, **kwargs):
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
    }).pack()
    Можно изменять текст через
    label['text'] = '123'
    """
    params = (
        'text', 'justify', # LEFT, RIGHT, CENTER
        'anchor',
        'width', 'height',
        'bg', 'fg',
        'bd', 'relief', # RAISED, SUNKEN
        'font', # Arial 20 italic | ('Comic Sans MS', 20, 'bold', 'underline')
        'padx', 'pady',
        'cursor',
        'image', # PhotoImage(file='logo.png')
        'underline', # 1 (не робит)
        'wraplength',
    )
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self):
        super().pack()
        return self


class Button(tk.Button, AbstractWidget):
    """Кнопка
    button = Button(root, **{
        'text': 'Жмакай', 'fg': 'lime', 'bg': 'black',
        'font': ('Arial', 20),
        'activebackground': 'red',
        #'state': 'DISABLED',
        'borderwidth': 10,
        'command': print, # функция
    }).pack()
    """
    params = (
        'activebackground',
        'state', # NORMAL, ACTIVE, DISABLED
        'borderwidth',
        'command',
    )
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self):
        super().pack()
        return self


class Entry(tk.Entry, AbstractWidget):
    """Ввод текста
    """
    params = (
    )
    def __init__(self, parent, **kwargs):
       super().__init__(parent, **self.check_kwargs(**kwargs))

    def pack(self):
        super().pack()
        return self

    def insert(self, start_index: int, text: str):
        """Вставка текста
           :param start_index: начальный индекс
           :param text: текст
        """
        super().insert(start_index, text)

    def delete(self, start_index: int, end_index: int):
        """Удаление текста
           :param start_index: начальный индекс
           :param end_index: конечный индекс
        """
        super().delete(start_index, end_index)

    def get(self):
        """Получение текста
        """
        return super().get()


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.tasks_canvas = tk.Canvas(self)
        self.tasks_frame = tk.Frame(self.tasks_canvas)
        self.text_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(
            self.tasks_canvas,
            orient='vertical',
            command=self.tasks_canvas.yview,
        )
        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title('TODO list')
        self.geometry('300x400')
        #self.label = tk.Label(self, text='hello world', padx=10, pady=10)
        #self.label.pack()

        self.tasks_create = tk.Text(
            self.text_frame,
            height=3,
            bg='white',
            fg='black',
        )
        self.tasks_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_frame = self.tasks_canvas.create_window(
            (0, 0),
            window=self.tasks_frame,
            anchor='n',
        )
        self.tasks_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.tasks_create.focus_set()

        todo1 = tk.Label(
            self.tasks_frame,
            text='--- Add items ---',
            bg='lightgrey',
            fg='black',
            pady=10,
        )
        todo1.bind('<Button-1>', self.remove_task)
        self.tasks.append(todo1)

        for task in self.tasks:
            task.pack(sid=tk.TOP, fill=tk.X)

        self.bind('<Return>', self.add_task)
        self.bind('<Configure>', self.on_frame_configure)
        self.bind_all('<MouseWheel>', self.mouse_scroll)
        self.bind_all('<Button-4>', self.mouse_scroll)
        self.bind_all('<Button-5>', self.mouse_scroll)
        self.tasks_canvas.bind('<Configure>', self.tasks_width)

        #self.task_create = tk.Text(
        #    self,
        #    height=3,
        #    bg='white',
        #    fg='black',
        #)
        #self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        #self.task_create.focus_set()

        self.colour_schemes = [{
            'bg': 'lightgrey',
            'fg': 'black',
        }, {
            'bg': 'grey',
            'fg': 'white',
        }]

    def add_task(self, event=None):
        task_text = self.tasks_create.get(1.0, tk.END).strip()
        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.set_task_colour(len(self.tasks), new_task)
            new_task.bind('<Button-1>', self.remove_task)

            #_, task_style_choice = divmod(len(self.tasks), 2)
            #my_scheme_choice = self.colour_schemes[task_style_choice]
            #new_task.configure(bg=my_scheme_choice['bg'])
            #new_task.configure(fg=my_scheme_choice['fg'])
            new_task.pack(side=tk.TOP, fill=tk.X)
            self.tasks.append(new_task)
        self.tasks_create.delete(1.0, tk.END)

    def remove_task(self, event):
        task = event.widget
        if msg.askyesno('Really delete?', 'Delete %s?' % task.cget('text')):
            self.tasks.remove(event.widget)
            event.widget.destroy()
            self.recolour_tasks()

    def recolour_tasks(self):
        for index, task in enumerate(self.tasks):
            self.set_task_colour(index, task)

    def set_task_colour(self, position, task):
        _, task_style_choice = divmod(position, 2)
        my_scheme_choice = self.colour_schemes[task_style_choice]
        task.configure(bg=my_scheme_choice['bg'])
        task.configure(fg=my_scheme_choice['fg'])

    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox('all'))

    def tasks_width(self, event):
        canvas_width = event.width
        self.tasks_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            self.tasks_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            self.tasks_canvas.yview_scroll(move, 'units')


if __name__ == '__main__':
    #root = Root()
    root = Window(**{
        'title': 'test', 'geometry': '300x300', 'resizable': (0, 0),
    })

    def new_label():
        label = Label(root, **{
            'text': 'ДРАТУЙ test\ntest2', 'fg': 'lime', 'bg': 'black',
            'cursor': 'man',
        }).pack()
        # entry должна быть создана до вызова
        label['text'] = entry.get()

    button = Button(root, **{
        'text': 'Жмакай', 'fg': 'lime', 'bg': 'black',
        'font': ('Arial', 20),
        'activebackground': 'red',
        #'state': 'DISABLED',
        'borderwidth': 10,
        'command': new_label, # функция
    }).pack()

    entry = Entry(root, **{
        'font': ('Arial', 20),
    }).pack()
    entry.insert(0, 'hello')
    entry.insert(5, 'world')
    entry.delete(0, 5)
    print(entry.get())


    root.mainloop()