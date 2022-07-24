import tkinter
from tkinter import *
import customtkinter
from pystray import MenuItem as item
from PIL import Image, ImageTk
from time import sleep
import pystray
import pyperclip
import keyboard

# Настраиваем свойства
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# Создаем окно приложения
main_window = customtkinter.CTk()
main_window.title("Simpless Clipboard")
main_window.configure(background="white")

# Устанавливам размер окна приложения
main_window.geometry("700x350")

# Создаем экземпляр буфера обмена
clipboard = pyperclip

# Создаем экземпляр списка
clipboard_list = Listbox(main_window, width=40, borderwidth=2, background="white", height=350)


# Выход из приложения
def quit_window(icon, item):
    icon.stop()
    main_window.destroy()


# Показать приложение
def show_window(icon, item):
    icon.stop()
    main_window.after(0, main_window.deiconify)


# Скрыть приложение
def hide_window():
    main_window.withdraw()
    image = Image.open('simpless_icon64.ico')
    menu = (item('Показать', show_window), item('Выход', quit_window))
    icon = pystray.Icon("name", image, "Иконка", menu)
    icon.run()


# Наполнение списка содержимым буфера обмена при нажатии Ctrl + C
def keyboard_pressed(event):
    if keyboard.is_pressed('ctrl'):
        sleep(0.2)
        current_clipboard_text = clipboard.paste()
        if current_clipboard_text and not current_clipboard_text.isspace():
            with open("clipboard_history.txt", "a") as file:
                file.write(current_clipboard_text.strip() + '\n')
                clipboard_list.insert(END, current_clipboard_text.strip())


def load_clipboard_history():
    with open("clipboard_history.txt", "r+") as file:
        for line in file:
            clipboard_list.insert(END, line.strip())


def clear_clipboard_history():
    with open("clipboard_history.txt", "r+") as file:
        file.truncate(0)
    clipboard_list.delete(0, END)


def double_click(event):
    for i in clipboard_list.curselection():
        clipboard.copy(clipboard_list.get(i))


# Создаем кнопки для управления

clear_clipboard_button = customtkinter.CTkButton(master=main_window, text="Очистить историю буфера обмена", width=120,
                                                 height=32,
                                                 border_width=0,
                                                 corner_radius=1, command=clear_clipboard_history)
clear_clipboard_button.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

if __name__ == '__main__':
    keyboard.on_press_key('c', keyboard_pressed)
    main_window.protocol('WM_DELETE_WINDOW', hide_window)
    clipboard_list.pack(expand=0)
    #clipboard_list.grid(row=0, column=0, sticky='nsew')
    clipboard_list.bind('<Double-Button-1>', double_click)
    clear_clipboard_button.pack()
    # clear_clipboard_button.config(command=clear_clipboard_history)
    load_clipboard_history()
    main_window.mainloop()
