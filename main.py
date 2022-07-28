from tkinter import *
from pystray import MenuItem as item
from PIL import Image
from time import sleep
import tkinter.messagebox
import pystray
import pyperclip
import keyboard
import os.path

# Создаем окно приложения
main_window = Tk()
main_window.title("Simpless Clipboard")
main_window.configure(background="white")
main_window.iconbitmap("simpless_icon64.ico")

# Создаем надпись с помощью
help_label = Label(text='Чтобы скопировать текст в буфер, дважды кликните по нему ЛКМ', background="white")

# Устанавливам размер окна приложения и отключаем изменение размера
main_window.geometry("400x260")
main_window.resizable(False, False)

# Создаем экземпляр буфера обмена
clipboard = pyperclip

# Создаем список с историей буфера обмена
clipboard_list = Listbox(main_window, width=85, borderwidth=0, background="white", height=10)

# Всплывающие сообщения
message_box = tkinter.messagebox


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
            with open("clipboard_history.txt", "a+") as file:
                file.write(current_clipboard_text.strip() + '\n')
                clipboard_list.insert(END, current_clipboard_text.strip())


# Загрузка содержимого файла с историей буфера обмена в программу
def load_clipboard_history():
    if os.path.exists("clipboard_history.txt"):
        with open("clipboard_history.txt", "r+") as file:
            clipboard_list.insert(END, file.readlines())


# Очистка истории буфера обмена
def clear_clipboard_history():
    with open("clipboard_history.txt", "r+") as file:
        file.truncate(0)
    clipboard_list.delete(0, END)


# Вставка содержимое истории в буфер обмена по двойному клику ЛКМ
def double_click(event):
    for i in clipboard_list.curselection():
        clipboard.copy(clipboard_list.get(i))
        message_box.showinfo("Текст скопирован", clipboard_list.get(i))


# Создаем кнопки для управления
clear_clipboard_button = Button(text="Очистить историю буфера обмена", width=50,
                                height=2, command=clear_clipboard_history)

if __name__ == '__main__':
    keyboard.on_press_key('c', keyboard_pressed)
    main_window.protocol('WM_DELETE_WINDOW', hide_window)
    clipboard_list.pack(side="top")
    clipboard_list.bind('<Double-Button-1>', double_click)
    clear_clipboard_button.pack(side="top", pady=10)
    help_label.pack(side="top")
    load_clipboard_history()
    main_window.mainloop()
