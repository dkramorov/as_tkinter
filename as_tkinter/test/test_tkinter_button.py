#!/usb/bin/env python3

import tkinter as tk
from tkinter import ttk


def game_over():
    print('well done')


def main():

    def on_motion(event):
        #print(event.x, event.y)
        x, y = button.winfo_x(), button.winfo_y()
        width, height = button.winfo_width(), button.winfo_height()
        print(x, y, width, height)

        leftx = x - 10
        rightx = x + width + 10
        topy = y - 10
        bottomy = y + height + 10

        near = False
        if event.x > leftx and event.x < rightx and event.y > topy and event.y < bottomy:
            near = True

        if near:
            if event.x > leftx and event.x < rightx:
                if event.x > x + width/2:
                    x = x - 10
                else:
                    x = x + 10
            if event.y > topy and event.y < bottomy:
                if event.y < y:
                    y = y + 10
                else:
                    y = y - 10
        button.place(x=x, y=y)

        print(near)


    root = tk.Tk()
    root.geometry('600x600')

    frame = ttk.Frame(root)
    frame.pack(expand=True, fill='both')
    frame.bind('<Motion>', on_motion)

    button = ttk.Button(frame, text='Жмакай', width=10, command=game_over)
    button.place(x=150, y=200)

    button2 = ttk.Button(frame, width=10, text='НЕ Жмакай')
    button2.place(x=300, y=200)

    root.mainloop()


if __name__ == '__main__':
    main()