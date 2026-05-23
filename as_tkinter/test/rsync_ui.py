import json
import os
import ttkbootstrap as ttk
import uuid

from managers.simple_logger import logger, json_pretty_print
from as_tkinter.abstract_widget import StringVar
from as_tkinter.tkinter_manager import (
    PhotoImage,
    Window,
    Panedwindow,
    Button,
    Label,
    Entry,
    Treeview,
    Canvas,
    Frame,
    ScrolledFrame,
    LabelFrame,
    Scrollbar,
)

"""
pip install tkreload
tkreload rsync_ui.py
"""


def create_images():
    """Создание изображений
       https://www.svgrepo.com/
    """
    from as_tkinter.svgs import save2file
    src_folder = '/Users/jocker/Downloads/123/FA'
    dst_folder = '/Users/jocker/Downloads/123/FA_PNG'
    btn_tasks = {
        'name': 'clipboard-list',
        'width': 24,
        'height': 24,
        'invert_colors': True,
        'fill': 'black',
        'stroke': 'black',
    }
    btn_add_task = {
        'name': 'plug-circle-plus',
        'width': 24,
        'height': 24,
        'invert_colors': True,
        'fill': 'black',
        'stroke': 'black',
    }
    btn_select_folder = {
        'name': 'folder-plus',
        'width': 24,
        'height': 24,
        'invert_colors': True,
        'fill': 'black',
        'stroke': 'black',
    }

    for item in (btn_tasks, btn_add_task, btn_select_folder):
        save2file(
            k=item['name'],
            fill=item['fill'],
            stroke=item['stroke'],
            invert_colors=item['invert_colors'],
            output_width=item['width'],
            output_height=item['height'],
        )


class App:
    def __init__(self):
        self.load_settings()
        self.root = Window(**self.settings)
        self.load_listeners()
        # TODO: для остальных стилей тоже задать
        self.style = ttk.Style('darkly')
        self.style.configure('dark.TButton', anchor='w')
        self.style.configure('secondary.TButton', anchor='w')

        self.add_task_form = []
        self.var_task_name = StringVar()
        self.var_src_folder = StringVar()
        self.var_dst_folder = StringVar()

        self.root.rowconfigure(index=0, weight=1, pad=20)
        self.root.columnconfigure(index=0, weight=0, minsize=200)
        self.root.columnconfigure(index=1, weight=1)
        self.root.columnconfigure(index=2, weight=0, minsize=200)
        self.create_section_menu()
        self.section_tasks = Panedwindow(self.root, **{
            'bootstyle': 'dark',
        }).grid(**{'row': 0, 'column': 1, 'sticky': 'nsew'})
        self.section_tasks.rowconfigure(index=0, weight=1)
        self.section_tasks.columnconfigure(index=0, weight=1)

        active_section = self.storage.get('active_section')
        if active_section == 'tasks':
            self.create_section_tasks()
        elif active_section == 'add_task':
            self.create_section_add_task()
        else:
            self.create_section_tasks()
        self.create_section_params()
        self.root.mainloop()

    def load_settings(self):
        """Загрузить настройки из хранилища"""
        storage = AppStorage()
        self.storage = storage
        self.img_folder = storage.get('img_folder') or '/Users/jocker/Downloads/123/FA_PNG'
        if not os.path.exists(self.img_folder):
            self.img_folder = '/tmp'
        self.title = storage.get('title') or 'rsync ui'
        self.window_info = '%sx%s+%s+%s' % (
            storage.get('width') or 800,
            storage.get('height') or 600,
            storage.get('x') or 5,
            storage.get('y') or 100,
        )
        self.theme = storage.get('theme') or 'darkly'
        self.settings = {
            'title': self.title,
            'geometry': self.window_info,
            'themename': self.theme,
        }

    def on_resize(self, event):
        """Масштабирование и перемещение виджета с отложенной записью результата
           :param event: событие
           :param widget: масштабируемый виджет
        """
        if not hasattr(self, 'after_cancel_id'):
            self.after_cancel_id = None
        if event.widget == self.root:
            if self.after_cancel_id:
                # Отмена отложенного действия
                self.root.after_cancel(self.after_cancel_id)
            # .after(func, arg1, arg2)
            self.after_cancel_id = self.root.after(1000, self.on_resized, event)

    def on_resized(self, event):
        if event.widget == self.root:
            self.storage.set('x', event.x)
            self.storage.set('y', event.y)
            self.storage.set('width', event.width)
            self.storage.set('height', event.height, save=True)

    def load_listeners(self):
        self.root.bind('<Configure>', self.on_resize)

    def create_section_menu(self):
        """Создание секции
        """
        self.section_menu = Panedwindow(self.root, **{
            'bootstyle': 'dark',
        }).grid(**{
            'row': 0, 'column': 0, 'sticky': 'nsew',
        })
        self.section_menu.columnconfigure(index=0, weight=1)
        self.section_menu.rowconfigure(index=0, weight=0)
        self.section_menu.rowconfigure(index=1, weight=0)
        self.section_menu.rowconfigure(index=2, weight=1)

        self.btn_tasks_image = PhotoImage(file='%s/clipboard-list.png' % self.img_folder)
        self.btn_tasks = Button(self.section_menu, **{
            'text': 'Задачи',
            'bootstyle': 'dark',
            'command': self.goto_tasks,
            'image': self.btn_tasks_image,
            'compound': 'left',
        }).grid(**{'row': 0, 'column': 0, 'sticky': 'ew'})
        self.btn_add_task_image = PhotoImage(file='%s/plug-circle-plus.png' % self.img_folder)
        self.btn_add_task = Button(self.section_menu, **{
            'text': 'Добавить задачу',
            'bootstyle': 'dark',
            'command': self.goto_add_task,
            'image': self.btn_add_task_image,
            'compound': 'left',
        }).grid(**{'row': 1, 'column': 0, 'sticky': 'ew'})

    def create_section_tasks(self):
        """Создание секции с выполняемыми задачами
           https://docs.python.org/3/library/tkinter.ttk.html#treeview
           https://ttkbootstrap.readthedocs.io/en/version-0.5/widgets/treeview.html
        """
        # ScrolledFrame не подходит для горизонтального скрола
        frame = ScrolledFrame(self.section_tasks, **{
            'autohide': False,
        })
        frame.grid(**{
            'row': 0, 'column': 0, 'sticky': 'nsew',
        })
        #hscroll = Scrollbar(frame, **{'orient': 'horizontal', 'command': frame.canvas.xview})
        """
        # Treeview не подходит для вывода задач
        tasks_columns = ('name', 'src', 'dst', 'drop')
        self.tasks_table = Treeview(self.section_tasks, **{
            'bootstyle': 'dark',
            'columns': tasks_columns,
            'show': 'headings',
        }).grid(**{'row': 0, 'column': 0, 'sticky': 'nsew', 'padx': 15})
        self.tasks_table.heading('name', text='Name')
        self.tasks_table.heading('src', text='Source')
        self.tasks_table.heading('dst', text='Destination')
        self.tasks_table.column('name', width=100, stretch=True)
        self.tasks_table.column('src', width=200, stretch=True)
        self.tasks_table.column('dst', width=200, stretch=True)
        self.tasks_table.column('drop', width=50, stretch=False)
        data = self.storage.get('tasks') or []
        for i, item in enumerate(data.keys()):
            task = data[item]
            self.tasks_table.insert('', i, values=(
                task['name'], task['src'], task['dst'],
            ), image=self.btn_drop_task_image)
        #self.tasks_table.bind('<<TreeviewSelect>>', self.task_select)
        self.tasks_table.bind('<Button-1>', self.task_select)
        """
        headers = ('#', 'Название', 'Источник', 'Назначение', 'Действия')
        row = 0
        for i, header in enumerate(headers):
            frame.rowconfigure(index=row, weight=0)
            frame.columnconfigure(index=i, weight=1)
            label = Label(frame, **{'text': header,}).grid(**{
                'row': row, 'column': i, 'sticky': 'ew',
            })
        data = self.storage.get('tasks') or []
        sorted_data = sorted(data.items(), key=lambda x: x[1]['position'])
        for i, data in enumerate(sorted_data):
            row += 1
            key, task = data[0], data[1]
            for i, header in enumerate(headers):
                content = ''
                if i == 0:
                    content = key
                elif i == 1:
                    content = task['name']
                elif i == 2:
                    content = task['src']
                elif i == 3:
                    content  = task['dst']
                label = Label(frame, **{
                    'text': content,
                }).grid(**{
                    'row': row, 'column': i, 'sticky': 'ew',
                })

    def create_section_add_task(self):
        """Создание секции с добавлением задачи
        """
        self.section_add_task = Panedwindow(self.section_tasks, **{
            'bootstyle': 'dark',
        }).grid(**{'row': 0, 'column': 0, 'sticky': 'nsew', 'padx': 15})
        self.section_add_task.columnconfigure(index=0, weight=1)

        self.add_task_form = [{
            'items': [{
                'component': Label,
                'props': {
                    'text': 'Название задачи',
                    'background': '#303030',
                },
                'pady': 0,
            }, {
                'name': 'name',
                'component': Entry,
                'props': {
                    'textvariable': self.var_task_name,
                },
                'pady': (0, 10),
                'el': None,
            }],
        }, {
            'items': [{
                'component': Label,
                'props': {
                    'text': 'Откуда',
                    'background': '#303030',
                },
                'pady': 0,
            }, {
                'name': 'src',
                'component': Entry,
                'props': {
                    'textvariable': self.var_src_folder,
                },
                'pady': (0, 10),
                'el': None,
            }],
        }, {
            'items': [{
                'component': Label,
                'props': {
                    'text': 'Куда',
                    'background': '#303030',
                },
                'pady': 0,
            }, {
                'name': 'dst',
                'component': Entry,
                'props': {
                    'textvariable': self.var_dst_folder,
                },
                'pady': (0, 10),
                'el': None,
            }],
        }, {
            'items': [{
                'component': Button,
                'props': {
                    'text': 'Сохранить',
                    'command': self.save_new_task,
                },
                'pady': 0,
            }],
        }]
        line_number = 0
        for fieldset in self.add_task_form:
            for item in fieldset['items']:
                self.section_add_task.rowconfigure(index=line_number, weight=0)
                item['el'] = item['component'](
                    self.section_add_task,
                    **item['props']
                ).grid(**{
                    'row': line_number,
                    'column': 0,
                    'sticky': 'ew',
                    'pady': item['pady'],
                })
                line_number += 1
        # Дополнительные кнопки вызова диалога выбора папки
        self.btn_select_folder_image = PhotoImage(file='%s/folder-plus.png' % self.img_folder)
        self.btn_select_folder_src = Button(self.section_add_task, **{
            'text': 'Выбрать',
            'bootstyle': 'dark',
            'command': lambda: self.select_folder(self.var_src_folder),
            'image': self.btn_select_folder_image,
        }).grid(**{'row': 3, 'column': 1, 'pady': (0, 10)})
        self.btn_select_folder_dst = Button(self.section_add_task, **{
            'text': 'Выбрать',
            'bootstyle': 'dark',
            'command': lambda: self.select_folder(self.var_dst_folder),
            'image': self.btn_select_folder_image,
        }).grid(**{'row': 5, 'column': 1, 'pady': (0, 10)})

    def create_section_params(self):
        """Создание секции
        """
        self.section_params = Panedwindow(self.root, **{
            'bootstyle': 'info',
        }).grid(**{'row': 0, 'column': 2, 'sticky': 'nsew'})
        btn = Button(self.section_params, **{'text': '123', 'command': self.get_color}).pack()

    def goto_tasks(self):
        """Открыть вкладку задач
        """
        self.btn_tasks.config(**{'bootstyle': 'secondary'})
        self.btn_add_task.config(**{'bootstyle': 'dark'})
        self.create_section_tasks()
        self.storage.set('active_section', 'tasks', save=True)

    def goto_add_task(self):
        """Открыть вкладку добавления задачи"""
        self.btn_tasks.config(**{'bootstyle': 'dark'})
        self.btn_add_task.config(**{'bootstyle': 'secondary'})
        self.create_section_add_task()
        self.storage.set('active_section', 'add_task', save=True)

    def get_color(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Select Color")
        if color[1]:
            print(f"Selected Hex: {color[1]}")

    def save_new_task(self):
        """Сохранение новой задачи
           TODO: валидацию на пустые поля
           TODO: валидацию на одинаковые src/dst
        """
        self.storage.save_new_task(
            name=self.var_task_name.get(),
            src=self.var_src_folder.get(),
            dst=self.var_dst_folder.get(),
        )

    def select_folder(self, var):
        """Выбор папки
           :param var: переменная куда пишем выбранную папку
        """
        from tkinter import filedialog
        #file_path = filedialog.askopenfilename(title="Select a File", initialdir="/", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            var.set(selected_folder)

    def task_select(self, event):
        """Выбор в таблице задач ячейки"""
        #selected_item = self.tasks_table.selection()[0]
        #item_values = self.tasks_table.item(selected_item, 'values')
        #print('selected row task %s' % (item_values, ))
        region = self.tasks_table.identify_region(event.x, event.y)
        if region == 'cell':
            column = self.tasks_table.identify_column(event.x)
            row = self.tasks_table.identify_row(event.y)
            print('click task: row %s column %s' % (row, column))


class AppStorage:
    """Хранилище для приложения
       обычный json файл
       TODO: вынести путь к файлу настроек в интерфейс
       TODO: сброс настроек
       TODO: копирование файла настроек в другое назначение
    """
    def __init__(self):
        self.db_folder = '/Users/jocker/Downloads/123'.rstrip('/')
        self.db_file = os.path.join(self.db_folder, 'db.json')
        self.data = {}
        self.load_data()

    def load_data(self):
        """Загрузить данные из хранилища
        """
        if not os.path.exists(self.db_file):
            return
        with open(self.db_file, 'r', encoding='utf-8') as f:
            self.data = json.loads(f.read())
        logger.info('LOAD: %s' % json_pretty_print(self.data))

    def save_data(self):
        """Сохранить данные в хранилище
        """
        with open(self.db_file, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(self.data))

    def get(self, key: str):
        """Получить значение из данных
           :param key: ключ
        """
        return self.data.get(key)

    def set(self, key: str, value: str, save: bool = False):
        """Записать значение в данные
           :param key: ключ
           :param value: значение
           :param save: сохранить в хранилище
        """
        self.data[key] = value
        if save:
            self.save_data()
            logger.info('SAVE: %s' % json_pretty_print(self.data))

    def save_new_task(self, name: str, src: str, dst: str):
        """Сохранение новой задачи
           :param name: название задачи
           :param src: исходная папка
           :param dst: папка назначения
        """
        if not self.data.get('tasks'):
            self.data['tasks'] = {}
        while True:
            # Не даем повторяться uid для задач
            new_uid = str(uuid.uuid4())
            if new_uid in self.data['tasks']:
                continue
            break
        self.data['tasks'][new_uid] = {
            'name': name,
            'src': src,
            'dst': dst,
            'position': len(self.data['tasks']),
        }
        self.save_data()

if __name__ == '__main__':
    #create_images()
    App()
