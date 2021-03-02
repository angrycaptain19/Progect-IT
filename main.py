from tkinter import *
import webbrowser
import urllib.request
import math
import time
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox as mb


class Interface:

    def __init__(self, master):
        self.master = master
        master.title('Thrown body trajectory')
        master.geometry('1000x700')
        master.configure(bg='blue')
        master.resizable(False, False)

        self.url = "https://www.webmath.ru/poleznoe/fizika/fizika_103_dvizhenie_tela_broshennogo_gorizontalno.php"
        self.zag = Label(self.master, text='Моделирование\n траектории движения брошенного тела', \
                         font='Verdana, 30', bg='blue', fg='yellow')
        self.zag.place(x=500, y=70, anchor='center')

        self.mb = Menubutton(self.master, text="Выберите тип броска", bg='green', bd='10', font='12') # создание кнопки МЕНЮ для выбора типа броска
        self.mb.menu = Menu(self.mb, tearoff=0)
        self.mb["menu"] = self.mb.menu
        self.mb.place(x=20, y=150, anchor='nw', height=50, width=230, bordermode=INSIDE)
        self.mb.menu.add_command(label="Под углом к горизонту", command=self.press) # создание подпунктов МЕНЮ для выбора типа броска
        self.mb.menu.add_separator()
        self.mb.menu.add_command(label="Горизонтально", command=self.press_1)
        self.mb.menu.add_separator()
        self.mb.menu.add_command(label="Вертикально вверх", command=self.press_2)
        self.mb.menu.add_separator()

        self.mb_vale = Menubutton(self.master, text="Введите данные", bg='green', bd='10', font='12', ) # создание кнопки МЕНЮ для ввода данных
        self.mb_vale.menu = Menu(self.mb_vale, tearoff=0)
        self.mb_vale["menu"] = self.mb_vale.menu
        self.mb_vale.place(x=20, y=240, anchor='nw', height=50, width=230, bordermode=INSIDE)
        self.mb_vale.menu.add_command(label="Ввести с клавиатуры", command=self.press_input) # создание подпунктов МЕНЮ для выбора способа ввода данных
        self.mb_vale.menu.add_separator()
        self.mb_vale.menu.add_command(label="Считать из файла", command=self.read_text)
        self.mb_vale.menu.add_separator()

        self.visualization = Button(self.master, text="Визуализация данных", bg='green', font='12',
                                    command=self.openGraphica)  # создание кнопки для вызова графического окна с визуализацией данных
        self.visualization.place(x=20, y=330, anchor='nw', height=50, width=230, bordermode=INSIDE)

        self.mb_info = Menubutton(self.master, text="Теория по теме", bg='green', bd='10', font='12', ) # создание кнопки МЕНЮ для выбора способа отображения теории по теме
        self.mb_info.menu = Menu(self.mb_info, tearoff=0)
        self.mb_info["menu"] = self.mb_info.menu
        self.mb_info.place(x=20, y=420, anchor='nw', height=50, width=230, bordermode=INSIDE)
        self.mb_info.menu.add_command(label="Информационный ресурс в браузере",
                                      command=lambda aurl=self.url: self.url_open(aurl))  # создание подпунктов МЕНЮ для выбора способа отображения теории по теме
        self.mb_info.menu.add_command(label="Ознакомиться в приложении", command=self.openDialog)
        self.mb_info.menu.add_separator()

        self.mb_save = Menubutton(self.master, text="Сохранить результат", bg='green', bd='10', font='12', ) # создание кнопки МЕНЮ для выбора способа сохранения результатов
        self.mb_save.menu = Menu(self.mb_save, tearoff=0)
        self.mb_save["menu"] = self.mb_save.menu
        self.mb_save.place(x=20, y=510, anchor='nw', height=50, width=230, bordermode=INSIDE)
        self.mb_save.menu.add_command(label="Сохранить в файл", command=self.file_save)  # создание подпунктов МЕНЮ для выбора способа сохранения результатов
        self.mb_save.menu.add_command(label="Выслать на электронную почту") # отсылка на электронную почту не реализована
        self.mb_save.menu.add_separator()

        self.subtitle = Label(self.master, text="Тип броска", font='Arial, 26', bg='blue', fg='chartreuse') # создание надписей на поле приложения
        self.subtitle.place(x=300, y=150, anchor='w')

        self.flight_duration = Label(self.master, text="Длительность полета\n (сек)", font='12', bg='blue', fg='white')
        self.flight_duration.place(x=300, y=240, anchor='w')

        self.b = DoubleVar()
        self.duration = Entry(self.master, font='12', textvariable=self.b) # создание однострочного текстового поля для ввода и вывода данных
        self.duration.configure(state="disable")
        self.duration.place(x=300, y=300, anchor='w')

        self.range_of_flight = Label(self.master, text="Дальность полета\n (м)", font='12', bg='blue', fg='white')
        self.range_of_flight.place(x=600, y=240, anchor='w')

        self.c = DoubleVar()
        self.rang = Entry(self.master, font='12', textvariable=self.c)
        self.rang.configure(state="disable")
        self.rang.place(x=600, y=300, anchor='w')

        self.flight_altitude = Label(self.master, text="Высота полета\n (м)", font='12', bg='blue', fg='white')
        self.flight_altitude.place(x=300, y=360, anchor='w')

        self.d = DoubleVar()
        self.altitude = Entry(self.master, font='12', textvariable=self.d)
        self.altitude.configure(state="disable")
        self.altitude.place(x=300, y=420, anchor='w')

        self.angle = Label(self.master, text="Угол под которым было\n брошено тело (°)", font='12', bg='blue',
                           fg='white')
        self.angle.place(x=600, y=360, anchor='w')

        self.j = DoubleVar()
        self.angle_val = Entry(self.master, font='12', textvariable=self.j)
        self.angle_val.configure(state="disable")
        self.angle_val.place(x=600, y=420, anchor='w')

        self.v = Label(self.master, text="Начальная скорость\n (м/с)", font='12', bg='blue', fg='white')
        self.v.place(x=300, y=480, anchor='w')

        self.a = DoubleVar()
        self.v_val = Entry(self.master, font='12', textvariable=self.a)
        self.v_val.configure(state="disable")
        self.v_val.place(x=300, y=540, anchor='w')

        self.h = Label(self.master, text="Начальная высота\n (м)", font='12', bg='blue', fg='white')
        self.h.place(x=600, y=480, anchor='w')

        self.k = DoubleVar()
        self.h_val = Entry(self.master, font='12', textvariable=self.k)
        self.h_val.configure(state="disable")
        self.h_val.place(x=600, y=540, anchor='w')

        self.calc = Button(self.master, text='РАСЧИТАТЬ', bg='chartreuse', font='12', command=self.calc)
        self.calc.place(x=500, y=630, anchor='e')

        self.discharge = Button(self.master, text='СБРОС', bg='chartreuse', font='12', command=self.clear_text)
        self.discharge.place(x=650, y=630, anchor='w')

        self.master.mainloop()

    def openDialog(self): # функция вызова дочернего окна с теоретической информацией
        Theory(self.master)

    def url_open(self, url): # функция перехода на веб страницу по ссылке
        webbrowser.open_new(url)

    def openGraphica(self): # функция создания дочернего окна с графикой
        self.create_canv()

    def press(self): # функция выбора типа броска (поля ввода неактивны)
        self.subtitle.configure(text="Тип броска: Под углом к горизонту")
        self.duration.configure(state='disable')
        self.rang.configure(state='disable')
        self.altitude.configure(state='disable')
        self.angle_val.configure(state='disable')
        self.v_val.configure(state='disable')
        self.h_val.configure(state='disable')

    def press_1(self): # # функция выбора типа броска (поля ввода неактивны)
        self.subtitle.configure(text="Тип броска: Горизонтально")
        self.duration.configure(state='disable')
        self.rang.configure(state='disable')
        self.altitude.configure(state='disable')
        self.angle_val.configure(state='disable')
        self.v_val.configure(state='disable')
        self.h_val.configure(state='disable')

    def press_2(self): # функция выбора типа броска (поля ввода неактивны)
        self.subtitle.configure(text="Тип броска: Вертикально вверх")
        self.duration.configure(state='disable')
        self.rang.configure(state='disable')
        self.altitude.configure(state='disable')
        self.angle_val.configure(state='disable')
        self.v_val.configure(state='disable')
        self.h_val.configure(state='disable')

    def press_input(self): # функция выбора ввода через клавиатуру (поля ввода становятся активны)
        if self.subtitle.cget('text') == "Тип броска: Под углом к горизонту":
            self.duration.configure(state='normal')
            self.rang.configure(state='normal')
            self.altitude.configure(state='normal')
            self.angle_val.configure(state='normal')
            self.v_val.configure(state='normal')

        if self.subtitle.cget('text') == "Тип броска: Горизонтально":
            self.altitude.configure(state='disable')
            self.angle_val.configure(state='disable')
            self.duration.configure(state='normal')
            self.rang.configure(state='normal')
            self.v_val.configure(state='normal')
            self.h_val.configure(state='normal')

        if self.subtitle.cget('text') == "Тип броска: Вертикально вверх":
            self.angle_val.configure(state='disable')
            self.rang.configure(state='disable')
            self.h_val.configure(state='disable')
            self.duration.configure(state='normal')
            self.v_val.configure(state='normal')
            self.altitude.configure(state='normal')

    def calc(self): # функция вычисления параметров
        self.v_n = self.a.get()
        self.t = self.b.get()
        self.h = self.d.get()
        self.h_n = self.k.get()
        self.angle = self.j.get()
        self.l = self.c.get()
        self.g = 9.81

        if self.subtitle.cget('text') == "Тип броска: Под углом к горизонту":
            if not self.a.get():  # нахождение начальной скорости
                if not self.b.get():
                    self.v_n = math.sqrt(self.l * self.g) / (
                            2 * math.sin(math.radians(self.angle)) * math.cos(math.radians(self.angle)))
                else:
                    self.v_n = (self.t * self.g) / (2 * math.cos(math.radians(self.angle)))
                self.a.set(self.v_n)
            if not self.b.get():  # нахождение времени
                if not self.a.get():
                    self.v_n = math.sqrt(self.l * self.g) / (2 * math.sin(math.radians(self.angle)) \
                                                             * math.cos(math.radians(self.angle)))
                self.t = 2 * self.v_n * (math.cos(math.radians(self.angle))) / self.g
                self.b.set(self.t)
            if not self.d.get():  # нахождение высоты
                if not self.a.get() and not self.b.get():
                    self.v_n = math.sqrt(self.l * self.g) / (2 * math.sin(math.radians(self.angle)) \
                                                             * math.cos(math.radians(self.angle)))
                    self.t = 2 * self.v_n * (math.cos(math.radians(self.angle))) / self.g
                elif not self.j.get():
                    cn = (self.t * self.g) / (2 * self.v_n)
                    self.angle = math.acos(cn) * (180 / math.pi)
                self.h = ((self.v_n) * (self.v_n) * ((1 - math.cos(math.radians(2 * self.angle))) / 2)) / (
                        2 * self.g)
                self.d.set(self.h)
            if not self.c.get():  # нахождение длины полета
                if not self.a.get() and self.j.get():
                    self.v_n = (self.t * self.g) / (2 * math.cos(math.radians(self.angle)))
                    self.l = ((self.v_n) ** 2) * (2 * math.sin(math.radians(self.angle)) \
                                                  * math.cos(math.radians(self.angle))) / self.g
                elif not self.j.get() and self.a.get():
                    cn = (self.t * self.g) / (2 * self.v_n)
                    self.angle1 = math.acos(cn) * (180 / math.pi)
                    self.l = ((self.v_n) ** 2) * (2 * math.sin(math.radians(self.angle1)) \
                                                  * math.cos(math.radians(self.angle1))) / self.g
                else:
                    self.l = ((self.v_n) ** 2) * (2 * math.sin(math.radians(self.angle)) \
                                                  * math.cos(math.radians(self.angle))) / self.g
                self.c.set(self.l)
            if not self.j.get():  # нахождение угла
                cn = (self.t * self.g) / (2 * self.v_n)
                self.angle = math.acos(cn) * (180 / math.pi)
                self.j.set(self.angle)

        if self.subtitle.cget('text') == "Тип броска: Горизонтально":
            if not self.a.get():  # нахождение начальной скорости
                self.v_n = (self.l / self.t)
                self.a.set(self.v_n)

            if not self.b.get():  # нахождение времени
                self.t = math.sqrt((2 * self.h_n) / self.g)
                self.b.set(self.t)

            if not self.k.get(): # нахождение начальной высоты
                self.h_n = (self.g * self.t) ** 2 / 2
                self.k.set(self.h_n)

            if not self.c.get(): # нахождение длины полета
                self.l = self.v_n * math.sqrt((2 * self.h_n) / self.g)
                self.c.set(self.l)

        if self.subtitle.cget('text') == "Тип броска: Вертикально вверх":
            if not self.a.get():  # нахождение начальной скорости
                self.v_n = self.t * self.g
                self.a.set(self.v_n)

            if not self.b.get():  # нахождение времени
                self.t = self.v_n / self.g
                self.b.set(self.t)

            if not self.d.get(): # нахождение высоты
                self.h = (self.v_n) ** 2 / (2 * self.g)
                self.d.set(self.h)
        return self.a

    def clear_text(self): # функция сброса значений в полях ввода
        self.a.set(0.0)
        self.b.set(0.0)
        self.c.set(0.0)
        self.d.set(0.0)
        self.j.set(0.0)
        self.k.set(0.0)

    def create_canv(self): # функция создания дочернего окна для графического изображения
        self.child_1 = Toplevel()
        self.child_1.title('Graphica')
        self.child_1.geometry('1000x700')
        self.child_1.resizable(False, False)

        self.canv = Canvas(self.child_1) # создание холста
        self.canv.configure(height=700, width=1000, bg='dodgerBlue')
        self.canv.pack()
        self.canv.create_line(30, 40, 30, 650, width=4, fill="black") # рисование осей координат
        self.canv.create_line(30, 40, 20, 50, width=4, fill="black")
        self.canv.create_line(30, 40, 40, 50, width=4, fill="black")
        self.canv.create_line(30, 650, 800, 650, width=4, fill="black")
        self.canv.create_line(800, 650, 790, 640, width=4, fill="black")
        self.canv.create_line(800, 650, 790, 660, width=4, fill="black")

        self.lb = Label(self.canv, text='Y', bg='dodgerBlue', fg='navy', font='16')
        self.lb.place(x=5, y=70, anchor='w')
        self.lb_1 = Label(self.canv, text='0', bg='dodgerBlue', fg='navy', font='16')
        self.lb_1.place(x=10, y=660, anchor='w')
        self.lb_2 = Label(self.canv, text='X', bg='dodgerBlue', fg='navy', font='16')
        self.lb_2.place(x=770, y=670, anchor='w')

        self.start = Button(self.canv, text='СТАРТ', bg='blue', fg='lavender', font='16', command=self.clickStart) # создание кнопки для начала анимации траектории полета тела
        self.start.place(x=830, y=650, anchor='w')

    def clickStart(self): # функция прорисовки (анимации) траектории полета тела
        self.sc = self.a.get() # считываем данные с полей ввода в переменные
        self.tim = self.b.get()
        self.heig = self.d.get()
        self.h_nach = self.k.get()
        self.angle1 = self.j.get()
        self.lon = self.c.get()
        self.gr = 9.81

        if self.subtitle.cget('text') == "Тип броска: Под углом к горизонту":
            self.scale = 0 # задаем масштабирование
            if self.sc <= 10:
                self.scale = 50
            elif 10 < self.sc <= 20:
                self.scale = 15
            elif 20 < self.sc <= 30:
                self.scale = 8
            elif 30 < self.sc <= 40:
                self.scale = 5
            elif 40 < self.sc < 90:
                self.scale = 3
            x = 30 # нулевая точка на оси Х
            y = 650 # нулевая точка на оси Y
            self.point = self.canv.create_oval(x - 7, y - 7, x + 7, y + 7, fill='green') # первая точка в траектории
            self.i = 0.2 # шаг времени
            self.x = 0
            self.y = 659
            self.ac = self.sc * math.cos(self.angle1 * math.pi / 180) * self.scale # константа для вычисления
            self.bc = self.sc * math.sin(self.angle1 * math.pi / 180) # константа для вычисления
            while self.x - 30 <= self.lon * self.scale - 30 or self.y < 630: # цикл для создания координат точкам и их прорисовка
                self.x = 30 + self.i * self.ac
                self.y = 650 - ((self.i * self.bc - self.gr * (self.i * self.i) / 2) * self.scale)
                self.point = self.canv.create_oval(self.x - 7, self.y - 7, self.x + 7, self.y + 7, fill='green')
                self.canv.update()
                time.sleep(0.2) # создаем задержку при прорисовки следующей точки, что создает эффект анимации
                self.i += 0.2
                self.canv.create_text(700, 60, text="Vo = (t * g) / (2 * cos(a))", justify=LEFT, font='Veranda, 18') # основные формулы расчетов
                self.canv.create_text(700, 100, text="t = 2 * Vo * cos(a) / g", justify=LEFT, font='Veranda, 18')
                self.canv.create_text(700, 140, text="n = Vo^2 * (1 - cos(2 * a) / 2) / (2 * g) ", justify=LEFT,
                                      font='Veranda, 18')
                self.canv.create_text(700, 180, text="L = 2 * Vo^2 * sin(a) * cos(a) / g", justify=LEFT,
                                      font='Veranda, 18')
                self.canv.create_text(700, 2200, text="a = acos(t * g / (2 * Vo)) * (180 / pi)", justify=LEFT,
                                      font='Veranda, 18')

        if self.subtitle.cget('text') == "Тип броска: Горизонтально":
            self.scale = 30
            if 5 < self.h_nach <= 20 and self.sc < 30:
                self.scale = 15
            elif 5 < self.h_nach <= 20 and self.sc > 30:
                self.scale = 10
            elif 20 < self.h_nach <= 30:
                self.scale = 10
            elif 30 < self.h_nach <= 40:
                self.scale = 50
            elif 40 < self.h_nach <= 50:
                self.scale = 3
            elif self.h_nach > 50:
                self.scale = 1

            x = 30
            y = 650 - (self.h_nach * self.scale)
            self.point = self.canv.create_oval(x - 7, y - 7, x + 7, y + 7, fill='green')
            self.i = 0.2
            self.x = 0
            self.y = 659
            while self.x - 30 <= self.lon * self.scale or self.y < 650:
                self.x = x + (self.sc * self.i * self.scale)
                self.y = 650 - (self.h_nach - (self.gr * (self.i * self.i)) / 2) * self.scale
                self.point = self.canv.create_oval(self.x - 7, self.y - 7, self.x + 7, self.y + 7, fill='green')
                self.canv.update()
                time.sleep(0.2)
                self.i += 0.2
                self.canv.create_text(800, 60, text="Vo = L / t", justify=LEFT, font='Veranda, 18')
                self.canv.create_text(800, 100, text="t = sqrt(2 *  ho) / g", justify=LEFT, font='Veranda, 18')
                self.canv.create_text(800, 140, text="no = (g * t)^2 / 2", justify=LEFT,
                                      font='Veranda, 18')
                self.canv.create_text(800, 180, text="L = Vo * sqrt(2 * ho/ g)", justify=LEFT,
                                      font='Veranda, 18')

        if self.subtitle.cget('text') == "Тип броска: Вертикально вверх":
            self.scale = 30
            if 5 < self.sc <= 20:
                self.scale = 15
            elif 20 < self.sc <= 30:
                self.scale = 10
            elif 30 < self.sc <= 40:
                self.scale = 6
            elif 40 < self.sc <= 50:
                self.scale = 3
            elif self.sc > 50:
                self.scale = 1

            x = 35
            y = 650
            self.point = self.canv.create_oval(x - 7, y - 7, x + 7, y + 7, fill='green')
            self.i = 0.2
            self.x = 0
            self.y = 650
            while self.x - 35 <= self.lon * self.scale or self.y < 650:
                self.x = x + (self.i * self.scale)
                self.y = 650 - (self.sc * self.i - self.gr * (self.i * self.i) / 2) * self.scale
                self.point = self.canv.create_oval(self.x - 7, self.y - 7, self.x + 7, self.y + 7, fill='green')
                self.canv.update()
                time.sleep(0.2)
                self.i += 0.2
                self.canv.create_text(800, 60, text="Vo = to / g", justify=LEFT, font='Veranda, 18')
                self.canv.create_text(800, 100, text="t = Vo / g", justify=LEFT, font='Veranda, 18')
                self.canv.create_text(800, 140, text="h = (Vo)^2 / 2 * g", justify=LEFT,
                                      font='Veranda, 18')

        self.child_1.grab_set()
        self.child_1.focus_set()
        self.child_1.wait_window()

    def file_save(self): # функция сохранения результатов вычисления в файл
        file_name = fd.asksaveasfilename(  # выбор файла или создание нового
            filetypes=(("TXT files", "*.txt"),
                       ("HTML files", "*.html;*.htm"),
                       ("All files", "*.*")))
        if self.subtitle.cget('text') == "Тип броска: Под углом к горизонту":  # подготовка строк
            s0 = ''
            s = "Длительность полета, (сек) - "
            s1 = self.duration.get()
            s2 = "Дальность полета, (м) - "
            s3 = self.rang.get()
            s4 = "Высота полета, (м) - "
            s5 = self.altitude.get()
            s6 = 'Угол под которым было брошено тело, (°) - '
            s7 = self.angle_val.get()
            s8 = "Начальная скорость, (м/с) - "
            s9 = self.v_val.get()
            lines = [s, s1, s0, s2, s3, s0, s4, s5, s0, s6, s7, s0, s8, s9]
        if self.subtitle.cget('text') == "Тип броска: Вертикально вверх":
            s0 = ''
            s = "Длительность полета, (сек) - "
            s1 = self.duration.get()
            s4 = "Высота полета, (м) - "
            s5 = self.altitude.get()
            s8 = "Начальная скорость, (м/с) - "
            s9 = self.v_val.get()
            s10 = "Начальная высота, (м) - "
            s11 = self.h_val.get()
            lines = [s, s1, s0, s4, s5, s0, s8, s9, s0, s10, s11]
        if self.subtitle.cget('text') == "Тип броска: Горизонтально":
            s0 = ''
            s = "Длительность полета, (сек) - "
            s1 = self.duration.get()
            s2 = "Дальность полета, (м) - "
            s3 = self.rang.get()
            s8 = "Начальная скорость, (м/с) - "
            s9 = self.v_val.get()
            s10 = "Начальная высота, (м)"
            s11 = self.h_val.get()
            lines = [s, s1, s0, s2, s3, s0, s8, s9, s0, s10, s11]
        with open(file_name, "w") as f: # открытие файла
            f.writelines("%s\n" % line for line in lines) # запись в файл

    def read_text(self): # функция считывания входных данных из файла
        self.press_input() # вызов функции для того, чтобы поля ввода стали активными
        file_name = fd.askopenfilename() # выбор файла
        s1 = 'Длительность полета, (сек) -'
        s2 = 'Дальность полета, (м) -'
        s3 = 'Высота полета, (м) -'
        s4 = 'Угол под которым было брошено тело, (°) -'
        s5 = 'Начальная скорость, (м/с) -'
        s6 = 'Начальная высота, (м)'
        f = open(file_name, "r", encoding='utf-8') # открытие файла
        s = list(map(str.strip, f.readlines())) # считывание всего файла в лист
        for i in range(len(s)): # выбор нужных значений и запись их в поля ввода данных
            a = s[i]
            if a == s1:
                self.duration.delete(0, 'end')
                self.duration.insert(INSERT, s[i + 1])
            if a == s2:
                self.rang.delete(0, 'end')
                self.rang.insert(INSERT, s[i + 1])
            if a == s3:
                self.altitude.delete(0, 'end')
                self.altitude.insert(INSERT, s[i + 1])
            if a == s4:
                self.angle_val.delete(0, 'end')
                self.angle_val.insert(INSERT, s[i + 1])
            if a == s5:
                self.v_val.delete(0, 'end')
                self.v_val.insert(INSERT, s[i + 1])
            if a == s6:
                self.h_val.delete(0, 'end')
                self.h_val.insert(INSERT, s[i + 1])
        f.close()


class Theory: # класс для ознакомления с теорий
    def __init__(self, master):
        self.child = Toplevel(master)
        self.child.title('Theory')
        self.child.geometry('1000x700')
        self.child.resizable(False, False)

        self.txt = ScrolledText(self.child, width=900, height=700, font='14', wrap=WORD, bg='plum') # создание текстового поля со скроллом
        self.txt.insert(INSERT, self.insert_text(self.txt)) # считывание с файла и запись в текстовое поле теоретического материала
        self.txt.configure(state='disabled')
        self.txt.pack()

        self.child.grab_set()
        self.child.focus_set()
        self.child.wait_window()

    def insert_text(self, txt): # функция считывания текста из файла и запись его в текстовое поле
        f = open('txt.txt', 'r', encoding='utf-8')
        s = f.readlines()
        for line in s:
            self.txt.insert(INSERT, line)
        return self.txt


win = Tk()
Interface(win)
