import tkinter as tk
from tkinter import font, filedialog
import fontawesome as fa
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json

from gui.util.config import TOP_BAR_COLOR, SIDE_MENU_COLOR, HOVER_MENU_CURSOR_COLOR, MAIN_BODY_COLOR
from gui.util import util_window, util_images
from src.model import ThermalAnalysis


class MainDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = util_images.read_image("gui/images/dsc_ret.jpeg", (560, 560))
        self.profile = util_images.read_image("gui/images/dsc_ret.jpeg", (20, 20))
        self.config_window()
        self.panels()
        self.top_bar_controls()
        self.side_menu_controls()
        self.sections_widgets = {
            'Dashboard': None,
            'Calculator': None,
            'Graphics': None,
            'Fit': None,
            'Results': None
        }
        self.loaded_files = {}
        self.file_paths = []
        self.file_listbox = tk.Listbox(borderwidth='1px', font=font.Font(family='FontAwesome', size=12),
                                       fg='#000000', justify='center', background='#e0d7d7')
        self.ta_objects = []
        self.fit_entries = []
        self.fit_entries_info = {1: {
            'x': 320,
            'y': 170,
            'width': 160,
            'height': 30,
            'text': 'a1'
        },
            2: {
                'x': 590,
                'y': 170,
                'width': 160,
                'height': 30,
                'text': 'b1'
            },
            3: {
                'x': 320,
                'y': 230,
                'width': 160,
                'height': 30,
                'text': 'c1'
            },
            4: {
                'x': 590,
                'y': 230,
                'width': 160,
                'height': 30,
                'text': 'd1'
            },
            5: {
                'x': 320,
                'y': 290,
                'width': 160,
                'height': 30,
                'text': 'a2'
            },
            6: {
                'x': 590,
                'y': 290,
                'width': 160,
                'height': 30,
                'text': 'b2'
            },
            7: {
                'x': 320,
                'y': 350,
                'width': 160,
                'height': 30,
                'text': 'c2'
            },
            8: {
                'x': 590,
                'y': 350,
                'width': 160,
                'height': 30,
                'text': 'd2'
            },
            9: {
                'x': 320,
                'y': 410,
                'width': 160,
                'height': 30,
                'text': 'a3'
            },
            10: {
                'x': 590,
                'y': 410,
                'width': 160,
                'height': 30,
                'text': 'b3'
            },
            11: {
                'x': 320,
                'y': 470,
                'width': 160,
                'height': 30,
                'text': 'c3'
            },
            12: {
                'x': 590,
                'y': 470,
                'width': 160,
                'height': 30,
                'text': 'd3'
            }
        }
        self.fit_selected_function = ""

    def config_window(self):

        self.title('DSC-TGA Analyzer')
        self.iconbitmap("gui/images/dsc_ret.ico")
        w, h = 1920, 1080
        util_window.center_window(self, w, h)

    def panels(self):

        self.top_bar = tk.Frame(
            self, bg=TOP_BAR_COLOR, height=50)
        self.top_bar.pack(side=tk.TOP, fill='both')

        self.side_menu = tk.Frame(
            self, bg=SIDE_MENU_COLOR, width=150)
        self.side_menu.pack(side=tk.LEFT, fill='both', expand=False)

        self.body = tk.Frame(
            self, bg=MAIN_BODY_COLOR)
        self.body.pack(side=tk.RIGHT, fill='both', expand=True)

    def create_entry(self, frame, borderwidth, font, foreground, justify, x, y, w, h, text):
        entry = tk.Entry(frame, borderwidth=borderwidth, font=font, fg=foreground, justify=justify)
        entry.insert(0, text)
        entry.bind("<FocusIn>", lambda event, entry=entry: self.on_entry_click(event, entry))
        entry.bind("<FocusOut>", lambda event, entry=entry, text=text: self.on_entry_leave(event, entry, text))
        entry.place(x=x, y=y, width=w, height=h)
        return entry

    def create_button(self, frame, x, y, w, h, text, font, borderwidth='1px', foreground='#000000', justify='center'):
        button = tk.Button(frame, borderwidth=borderwidth, font=font, fg=foreground, justify=justify, text=text)
        button.place(x=x, y=y, width=w, height=h)
        return button

    def create_listbox(self, frame, x, y, w, h, font, borderwidth='1px', foreground='#000000', justify='left', background="#e0d7d7"):
        listbox = tk.Listbox(frame, borderwidth=borderwidth, font=font, fg=foreground, justify=justify,
                             background=background)
        listbox.place(x=x, y=y, width=w, height=h)
        return listbox

    def create_label(self, frame, x, y, w, h, font, text, foreground='#000000', justify='left'):
        label = tk.Label(frame, font=font, justify=justify, text=text, foreground=foreground)
        label.place(x=x, y=y, width=w, height=h)
        return label

    def dashboard_body1(self):

        dashboard_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        dashboard_frame.config(width=874, height=550)

        ft = font.Font(family='FontAwesome', size=12)  # Marco para la lista de archivos

        files_list_box = tk.Listbox(dashboard_frame)
        files_list_box["borderwidth"] = "1px"
        files_list_box["font"] = ft
        files_list_box["fg"] = "#333333"
        files_list_box["justify"] = "center"
        files_list_box.place(x=50, y=60, width=360, height=350)

        files_info_listbox = tk.Listbox(dashboard_frame)
        files_info_listbox["borderwidth"] = "1px"
        files_info_listbox["font"] = ft
        files_info_listbox["fg"] = "#333333"
        files_info_listbox["justify"] = "center"
        files_info_listbox.place(x=464, y=60, width=360, height=420)

        add_file_button = tk.Button(dashboard_frame)
        add_file_button["bg"] = "#f0f0f0"
        add_file_button["font"] = ft
        add_file_button["fg"] = "#000000"
        add_file_button["justify"] = "center"
        add_file_button["text"] = "Añadir archivo"
        add_file_button.place(x=50, y=440, width=99, height=38)
        add_file_button["command"] = lambda: self.add_file(files_list_box)

        remove_file_button = tk.Button(dashboard_frame)
        remove_file_button["bg"] = "#f0f0f0"
        remove_file_button["font"] = ft
        remove_file_button["fg"] = "#000000"
        remove_file_button["justify"] = "center"
        remove_file_button["text"] = "Eliminar archivo"
        remove_file_button.place(x=180, y=440, width=99, height=38)
        remove_file_button["command"] = lambda: self.delete_file(files_list_box)

        show_info_button = tk.Button(dashboard_frame)
        show_info_button["bg"] = "#f0f0f0"
        show_info_button["font"] = ft
        show_info_button["fg"] = "#000000"
        show_info_button["justify"] = "center"
        show_info_button["text"] = "Mostrar información"
        show_info_button.place(x=310, y=440, width=99, height=38)
        show_info_button["command"] = self.show_file_info

        GLabel_753 = tk.Label(dashboard_frame)
        GLabel_753["font"] = ft
        GLabel_753["fg"] = "#333333"
        GLabel_753["justify"] = "center"
        GLabel_753["text"] = "Lista de archivos"
        GLabel_753.place(x=50, y=20, width=361, height=30)

        GLabel_735 = tk.Label(dashboard_frame)
        GLabel_735["font"] = ft
        GLabel_735["fg"] = "#333333"
        GLabel_735["justify"] = "center"
        GLabel_735["text"] = "Información del archivo"
        GLabel_735.place(x=460, y=20, width=365, height=30)

        return dashboard_frame

    def dashboard_body(self):

        width = 1770
        height = 1030

        dashboard_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        dashboard_frame.config(width=width, height=height)

        ft = font.Font(family='FontAwesome', size=12)

        self.file_listbox.place(x=80, y=80, width=163, height=580, in_=dashboard_frame)

        self.create_label(dashboard_frame, 80, 30, 160, 40, ft, text='File list')

        add_file_button = self.create_button(dashboard_frame, 80, 690, 150, 30, 'Add file', ft)
        add_file_button['command'] = lambda: self.add_file(self.file_listbox)

        delete_file_button = self.create_button(dashboard_frame, 80, 740, 150, 30, 'Delete file', ft)
        delete_file_button['command'] = lambda: self.delete_file(self.file_listbox)

        GButton_19 = tk.Button(dashboard_frame)
        GButton_19["bg"] = "#f0f0f0"
        GButton_19["font"] = ft
        GButton_19["fg"] = "#000000"
        GButton_19["justify"] = "center"
        GButton_19["text"] = "Show file info"
        GButton_19.place(x=80, y=790, width=150, height=30)
        GButton_19["command"] = self.GButton_19_command

        file_info_box = tk.Text(dashboard_frame)
        file_info_box["bg"] = "#e0d7d7"
        file_info_box["borderwidth"] = "1px"
        file_info_box["font"] = ft
        file_info_box["fg"] = "#333333"
        #GListBox_363["justify"] = "left"
        file_info_box.place(x=320, y=80, width=432, height=834)
        file_info_box.configure(state='disabled')

        scrollbar = tk.Scrollbar(dashboard_frame, command=file_info_box.yview)
        scrollbar.place(x=732, y=80, width=20, height=834)

        file_info_box.config(yscrollcommand=scrollbar.set)

        fig, ax = plt.subplots()
        ax2 = ax.twinx()

        canvas = FigureCanvasTkAgg(fig, master=dashboard_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=1030, y=80, width=548, height=472)

        show_file_info_button = self.create_button(dashboard_frame, 80, 790, 150, 30, 'Show file info', ft)
        show_file_info_button['command'] = lambda: self.show_file_info(self.file_listbox, file_info_box, fig, ax, ax2, canvas)

        GLabel_662 = tk.Label(dashboard_frame)
        GLabel_662["font"] = ft
        GLabel_662["fg"] = "#333333"
        GLabel_662["justify"] = "center"
        GLabel_662["text"] = "File info"
        GLabel_662["fg"] = "#333333"
        GLabel_662.place(x=320, y=30, width=433, height=40)

        GButton_290 = tk.Button(dashboard_frame)
        GButton_290["bg"] = "#f0f0f0"
        GButton_290["font"] = ft
        GButton_290["fg"] = "#000000"
        GButton_290["justify"] = "center"
        GButton_290["text"] = "Help"
        GButton_290.place(x=80, y=880, width=150, height=30)
        GButton_290["command"] = self.GButton_290_command

        self.dashboard_console = tk.Text(dashboard_frame)
        self.dashboard_console["bg"] = "#ffffff"
        self.dashboard_console["borderwidth"] = "1px"
        self.dashboard_console["font"] = font.Font(family='FontAwesome', size=9)
        self.dashboard_console["fg"] = "#333333"
        #GListBox_753["justify"] = "center"
        self.dashboard_console.place(x=850, y=710, width=738, height=204)
        self.dashboard_console.configure(state='disabled')

        return dashboard_frame

    def GButton_768_command(self):
        print("command")

    def GButton_125_command(self):
        print("command")

    def GButton_19_command(self):
        print("command")

    def GButton_290_command(self):
        print("command")

    def calculator_body(self):
        width = 1770
        height = 1030

        calculator_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        calculator_frame.config(width=width, height=height)

        ft = font.Font(family='FontAwesome', size=12)

        GLabel_868 = tk.Label(calculator_frame)
        GLabel_868["font"] = ft
        GLabel_868["fg"] = "#333333"
        GLabel_868["justify"] = "center"
        GLabel_868["text"] = "File list"
        GLabel_868.place(x=80, y=30, width=160, height=40)

        GButton_768 = tk.Button(calculator_frame)
        GButton_768["bg"] = "#f0f0f0"
        GButton_768["font"] = ft
        GButton_768["fg"] = "#000000"
        GButton_768["justify"] = "center"
        GButton_768["text"] = "Select file"
        GButton_768.place(x=80, y=690, width=150, height=30)
        GButton_768["command"] = self.GButton_768_command

        GListBox_363 = tk.Listbox(calculator_frame)
        GListBox_363["bg"] = "#e0d7d7"
        GListBox_363["borderwidth"] = "1px"
        GListBox_363["font"] = ft
        GListBox_363["fg"] = "#333333"
        GListBox_363["justify"] = "left"
        GListBox_363.place(x=320, y=80, width=432, height=834)

        fig, ax = plt.subplots()

        canvas = FigureCanvasTkAgg(fig, master=calculator_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=1030, y=80, width=548, height=472)

        GLabel_662 = tk.Label(calculator_frame)
        GLabel_662["font"] = ft
        GLabel_662["fg"] = "#333333"
        GLabel_662["justify"] = "center"
        GLabel_662["text"] = "Calculations and file info"
        GLabel_662.place(x=320, y=30, width=433, height=40)

        GButton_290 = tk.Button(calculator_frame)
        GButton_290["bg"] = "#f0f0f0"
        GButton_290["font"] = ft
        GButton_290["fg"] = "#000000"
        GButton_290["justify"] = "center"
        GButton_290["text"] = "Help"
        GButton_290.place(x=80, y=880, width=150, height=30)
        GButton_290["command"] = self.GButton_290_command

        GListBox_753 = tk.Listbox(calculator_frame)
        GListBox_753["bg"] = "#ffffff"
        GListBox_753["borderwidth"] = "1px"
        GListBox_753["font"] = ft
        GListBox_753["fg"] = "#333333"
        GListBox_753["justify"] = "center"
        GListBox_753.place(x=1030, y=710, width=558, height=204)

        GLineEdit_51 = tk.Entry(calculator_frame)
        GLineEdit_51["borderwidth"] = "1px"
        GLineEdit_51["font"] = ft
        GLineEdit_51["fg"] = "#333333"
        GLineEdit_51["justify"] = "center"
        GLineEdit_51.place(x=810, y=170, width=160, height=30)

        GLineEdit_534 = tk.Entry(calculator_frame)
        GLineEdit_534["borderwidth"] = "1px"
        GLineEdit_534["font"] = ft
        GLineEdit_534["fg"] = "#333333"
        GLineEdit_534["justify"] = "center"
        GLineEdit_534.place(x=810, y=230, width=161, height=30)

        GLineEdit_713 = tk.Entry(calculator_frame)
        GLineEdit_713["borderwidth"] = "1px"
        GLineEdit_713["font"] = ft
        GLineEdit_713["fg"] = "#333333"
        GLineEdit_713["justify"] = "center"
        GLineEdit_713.place(x=810, y=290, width=160, height=30)

        GLineEdit_965 = tk.Entry(calculator_frame)
        GLineEdit_965["borderwidth"] = "1px"
        GLineEdit_965["font"] = ft
        GLineEdit_965["fg"] = "#333333"
        GLineEdit_965["justify"] = "center"
        GLineEdit_965.place(x=810, y=350, width=160, height=30)

        GLineEdit_78 = tk.Entry(calculator_frame)
        GLineEdit_78["borderwidth"] = "1px"
        GLineEdit_78["font"] = ft
        GLineEdit_78["fg"] = "#333333"
        GLineEdit_78["justify"] = "center"
        GLineEdit_78.place(x=810, y=410, width=160, height=30)

        button_enter_temperatures = tk.Button(calculator_frame)
        button_enter_temperatures["bg"] = "#f0f0f0"
        button_enter_temperatures["font"] = ft
        button_enter_temperatures["fg"] = "#000000"
        button_enter_temperatures["justify"] = "center"
        button_enter_temperatures["text"] = "Calculate"
        button_enter_temperatures.place(x=815, y=470, width=150, height=30)
        button_enter_temperatures["command"] = self.GButton_290_command

        GLabel_256 = tk.Label(calculator_frame)
        GLabel_256["font"] = ft
        GLabel_256["fg"] = "#333333"
        GLabel_256["justify"] = "center"
        GLabel_256["text"] = "Input temperatures"
        GLabel_256.place(x=800, y=110, width=180, height=30)

        return calculator_frame

    def calculator_body1(self):
        # Marco principal para el cuerpo de la calculadora
        calculator_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        calculator_frame.config(width=874, height=550)

        ft = font.Font(family='FontAwesome', size=12)  # Marco para la lista de archivos

        files_list_box = tk.Listbox(calculator_frame)
        files_list_box["borderwidth"] = "1px"
        files_list_box["font"] = ft
        files_list_box["fg"] = "#333333"
        files_list_box["justify"] = "center"
        files_list_box.place(x=50, y=60, width=159, height=392)

        GLabel_938 = tk.Label(calculator_frame)
        GLabel_938["font"] = ft
        GLabel_938["fg"] = "#333333"
        GLabel_938["justify"] = "center"
        GLabel_938["text"] = "Lista de archivos"
        GLabel_938.place(x=50, y=20, width=157, height=30)

        calc_info = tk.Listbox(calculator_frame)
        calc_info["borderwidth"] = "1px"
        calc_info["font"] = ft
        calc_info["fg"] = "#333333"
        calc_info["justify"] = "center"
        calc_info.place(x=240, y=60, width=275, height=390)

        GLabel_419 = tk.Label(calculator_frame)
        GLabel_419["font"] = ft
        GLabel_419["fg"] = "#333333"
        GLabel_419["justify"] = "center"
        GLabel_419["text"] = "Cálculos"
        GLabel_419.place(x=240, y=20, width=277, height=32)

        button_realize_calc = tk.Button(calculator_frame)
        button_realize_calc["bg"] = "#f0f0f0"
        button_realize_calc["font"] = ft
        button_realize_calc["fg"] = "#000000"
        button_realize_calc["justify"] = "center"
        button_realize_calc["text"] = "Realizar cálculos"
        button_realize_calc.place(x=300, y=470, width=154, height=39)
        button_realize_calc["command"] = self.realize_calc

        select_file = tk.Button(calculator_frame)
        select_file["bg"] = "#f0f0f0"
        select_file["font"] = ft
        select_file["fg"] = "#000000"
        select_file["justify"] = "center"
        select_file["text"] = "Seleccionar archivo"
        select_file.place(x=50, y=470, width=156, height=39)
        select_file["command"] = self.select_file

        entry_first_index = tk.Entry(calculator_frame)
        entry_first_index["borderwidth"] = "1px"
        entry_first_index["font"] = ft
        entry_first_index["fg"] = "#333333"
        entry_first_index["justify"] = "left"
        entry_first_index["text"] = "Primer valor"
        entry_first_index.place(x=570, y=300, width=93, height=30)

        entry_second_index = tk.Entry(calculator_frame)
        entry_second_index["borderwidth"] = "1px"
        entry_second_index["font"] = ft
        entry_second_index["fg"] = "#333333"
        entry_second_index["justify"] = "left"
        entry_second_index["text"] = "Segundo valor"
        entry_second_index.place(x=720, y=300, width=93, height=30)

        entry_third_index = tk.Entry(calculator_frame)
        entry_third_index["borderwidth"] = "1px"
        entry_third_index["font"] = ft
        entry_third_index["fg"] = "#333333"
        entry_third_index["justify"] = "left"
        entry_third_index["text"] = "Tercer valor"
        entry_third_index.place(x=570, y=350, width=92, height=30)

        entry_fourth_index = tk.Entry(calculator_frame)
        entry_fourth_index["borderwidth"] = "1px"
        entry_fourth_index["font"] = ft
        entry_fourth_index["fg"] = "#333333"
        entry_fourth_index["justify"] = "left"
        entry_fourth_index["text"] = "Cuarto valor"
        entry_fourth_index.place(x=720, y=350, width=94, height=30)

        entry_fifth_index = tk.Entry(calculator_frame)
        entry_fifth_index["borderwidth"] = "1px"
        entry_fifth_index["font"] = ft
        entry_fifth_index["fg"] = "#333333"
        entry_fifth_index["justify"] = "left"
        entry_fifth_index["text"] = "Quinto valor"
        entry_fifth_index.place(x=570, y=400, width=93, height=30)

        button_graphic_calc = tk.Button(calculator_frame)
        button_graphic_calc["bg"] = "#f0f0f0"
        button_graphic_calc["font"] = ft
        button_graphic_calc["fg"] = "#000000"
        button_graphic_calc["justify"] = "center"
        button_graphic_calc["text"] = "Realizar cálculos gráficos"
        button_graphic_calc.place(x=590, y=470, width=193, height=40)
        button_graphic_calc["command"] = self.graphic_calc

        return calculator_frame

    def graphics_body(self):

        width = 1770
        height = 1030
        ft = font.Font(family='FontAwesome', size=12)

        graphics_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        graphics_frame.config(width=width, height=height)

        GListBox_389 = tk.Listbox(graphics_frame)
        GListBox_389["borderwidth"] = "1px"
        GListBox_389["font"] = ft
        GListBox_389["fg"] = "#333333"
        GListBox_389["justify"] = "center"
        GListBox_389.place(x=1030, y=80, width=548, height=472)

        GButton_290 = tk.Button(graphics_frame)
        GButton_290["bg"] = "#f0f0f0"
        GButton_290["font"] = ft
        GButton_290["fg"] = "#000000"
        GButton_290["justify"] = "center"
        GButton_290["text"] = "Help"
        GButton_290.place(x=80, y=880, width=150, height=30)
        GButton_290["command"] = self.GButton_290_command

        GListBox_753 = tk.Listbox(graphics_frame)
        GListBox_753["bg"] = "#ffffff"
        GListBox_753["borderwidth"] = "1px"
        GListBox_753["font"] = ft
        GListBox_753["fg"] = "#333333"
        GListBox_753["justify"] = "center"
        GListBox_753.place(x=1030, y=710, width=558, height=204)

        GLabel_901 = tk.Label(graphics_frame)
        GLabel_901["font"] = ft
        GLabel_901["fg"] = "#333333"
        GLabel_901["justify"] = "center"
        GLabel_901["text"] = "Figure list"
        GLabel_901.place(x=80, y=30, width=160, height=40)

        GLabel_515 = tk.Label(graphics_frame)
        GLabel_515["font"] = ft
        GLabel_515["fg"] = "#333333"
        GLabel_515["justify"] = "center"
        GLabel_515["text"] = "Plot"
        GLabel_515.place(x=330, y=450, width=350, height=40)

        # GButton_336 = tk.Button(graphics_frame)
        # GButton_336["bg"] = "#f0f0f0"
        # GButton_336["font"] = ft
        # GButton_336["fg"] = "#000000"
        # GButton_336["justify"] = "center"
        # GButton_336["text"] = "Language"
        # GButton_336.place(x=330, y=100, width=150, height=30)
        # GButton_336["command"] = self.GButton_336_command

        languages = ["English", "Español", "Galego"]
        selected_language = tk.StringVar(graphics_frame)
        selected_language.set(languages[0])

        # Función para cambiar el idioma seleccionado
        def change_language(*args):
            print(f"Idioma seleccionado: {selected_language.get()}")

        # Crear el menú desplegable
        GButton_336 = tk.OptionMenu(graphics_frame, selected_language, *languages, command=change_language)
        GButton_336.place(x=330, y=100, width=150, height=30)

        GButton_645 = tk.Button(graphics_frame)
        GButton_645["bg"] = "#f0f0f0"
        GButton_645["font"] = ft
        GButton_645["fg"] = "#000000"
        GButton_645["justify"] = "center"
        GButton_645["text"] = "Legend"
        GButton_645.place(x=530, y=100, width=150, height=30)
        GButton_645["command"] = self.GButton_645_command

        GButton_780 = tk.Button(graphics_frame)
        GButton_780["bg"] = "#f0f0f0"
        GButton_780["font"] = ft
        GButton_780["fg"] = "#000000"
        GButton_780["justify"] = "center"
        GButton_780["text"] = "Apply"
        GButton_780.place(x=420, y=320, width=150, height=30)
        GButton_780["command"] = self.GButton_780_command

        GButton_205 = tk.Button(graphics_frame)
        GButton_205["bg"] = "#f0f0f0"
        GButton_205["font"] = ft
        GButton_205["fg"] = "#000000"
        GButton_205["justify"] = "center"
        GButton_205["text"] = "New figure"
        GButton_205.place(x=80, y=590, width=160, height=30)
        GButton_205["command"] = self.GButton_205_command

        GLineEdit_977 = tk.Entry(graphics_frame)
        GLineEdit_977["borderwidth"] = "1px"
        GLineEdit_977["font"] = ft
        GLineEdit_977["fg"] = "#333333"
        GLineEdit_977["justify"] = "center"
        GLineEdit_977["text"] = "Entry"
        GLineEdit_977.place(x=530, y=230, width=150, height=30)

        GLineEdit_0 = tk.Entry(graphics_frame)
        GLineEdit_0["borderwidth"] = "1px"
        GLineEdit_0["font"] = ft
        GLineEdit_0["fg"] = "#333333"
        GLineEdit_0["justify"] = "center"
        GLineEdit_0["text"] = "Entry"
        GLineEdit_0.place(x=530, y=160, width=150, height=30)

        GLineEdit_727 = tk.Entry(graphics_frame)
        GLineEdit_727["borderwidth"] = "1px"
        GLineEdit_727["font"] = ft
        GLineEdit_727["fg"] = "#333333"
        GLineEdit_727["justify"] = "center"
        GLineEdit_727["text"] = "Entry"
        GLineEdit_727.place(x=330, y=160, width=150, height=30)

        GLineEdit_1 = tk.Entry(graphics_frame)
        GLineEdit_1["borderwidth"] = "1px"
        GLineEdit_1["font"] = ft
        GLineEdit_1["fg"] = "#333333"
        GLineEdit_1["justify"] = "center"
        GLineEdit_1["text"] = "Entry"
        GLineEdit_1.place(x=330, y=230, width=150, height=30)

        GListBox_913 = tk.Listbox(graphics_frame)
        GListBox_913["borderwidth"] = "1px"
        GListBox_913["font"] = ft
        GListBox_913["fg"] = "#333333"
        GListBox_913["justify"] = "center"
        GListBox_913.place(x=80, y=100, width=160, height=450)

        GLabel_843 = tk.Label(graphics_frame)
        GLabel_843["font"] = ft
        GLabel_843["fg"] = "#333333"
        GLabel_843["justify"] = "center"
        GLabel_843["text"] = "Figure parameters"
        GLabel_843.place(x=330, y=30, width=350, height=40)

        GButton_547 = tk.Button(graphics_frame)
        GButton_547["bg"] = "#f0f0f0"
        GButton_547["font"] = ft
        GButton_547["fg"] = "#000000"
        GButton_547["justify"] = "center"
        GButton_547["text"] = "Delete figure"
        GButton_547.place(x=80, y=650, width=160, height=30)
        GButton_547["command"] = self.GButton_547_command

        GButton_490 = tk.Button(graphics_frame)
        GButton_490["bg"] = "#f0f0f0"
        GButton_490["font"] = ft
        GButton_490["fg"] = "#000000"
        GButton_490["justify"] = "center"
        GButton_490["text"] = "Select figure"
        GButton_490.place(x=80, y=710, width=160, height=30)
        GButton_490["command"] = self.GButton_490_command

        GButton_64 = tk.Button(graphics_frame)
        GButton_64["bg"] = "#f0f0f0"
        GButton_64["font"] = ft
        GButton_64["fg"] = "#000000"
        GButton_64["justify"] = "center"
        GButton_64["text"] = "File"
        GButton_64.place(x=330, y=520, width=150, height=30)
        GButton_64["command"] = self.GButton_64_command

        GButton_542 = tk.Button(graphics_frame)
        GButton_542["bg"] = "#f0f0f0"
        GButton_542["font"] = ft
        GButton_542["fg"] = "#000000"
        GButton_542["justify"] = "center"
        GButton_542["text"] = "What to plot?"
        GButton_542.place(x=530, y=520, width=150, height=30)
        GButton_542["command"] = self.GButton_542_command

        GButton_651 = tk.Button(graphics_frame)
        GButton_651["bg"] = "#f0f0f0"
        GButton_651["font"] = ft
        GButton_651["fg"] = "#000000"
        GButton_651["justify"] = "center"
        GButton_651["text"] = "Color"
        GButton_651.place(x=330, y=640, width=150, height=30)
        GButton_651["command"] = self.GButton_651_command

        GButton_813 = tk.Button(graphics_frame)
        GButton_813["bg"] = "#f0f0f0"
        GButton_813["font"] = ft
        GButton_813["fg"] = "#000000"
        GButton_813["justify"] = "center"
        GButton_813["text"] = "Linestyle"
        GButton_813.place(x=330, y=580, width=150, height=30)
        GButton_813["command"] = self.GButton_813_command

        GLineEdit_62 = tk.Entry(graphics_frame)
        GLineEdit_62["borderwidth"] = "1px"
        GLineEdit_62["font"] = ft
        GLineEdit_62["fg"] = "#333333"
        GLineEdit_62["justify"] = "center"
        GLineEdit_62["text"] = "Linewidth"
        GLineEdit_62.place(x=530, y=580, width=150, height=30)

        GButton_754 = tk.Button(graphics_frame)
        GButton_754["bg"] = "#e0d7d7"
        GButton_754["font"] = ft
        GButton_754["fg"] = "#000000"
        GButton_754["justify"] = "center"
        GButton_754["text"] = "Plot"
        GButton_754.place(x=530, y=640, width=150, height=30)
        GButton_754["command"] = self.GButton_754_command

        GButton_813 = tk.Button(graphics_frame)
        GButton_813["bg"] = "#f0f0f0"
        GButton_813["font"] = ft
        GButton_813["fg"] = "#000000"
        GButton_813["justify"] = "center"
        GButton_813["text"] = "Save figure"
        GButton_813.place(x=1230, y=580, width=150, height=30)
        GButton_813["command"] = self.GButton_813_command

        return graphics_frame

    def fit_body(self):

        width = 1770
        height = 1030

        fit_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        fit_frame.config(width=width, height=height)

        ft = font.Font(family='FontAwesome', size=12)

        GListBox_108 = tk.Listbox(fit_frame)
        GListBox_108["bg"] = "#e0d7d7"
        GListBox_108["borderwidth"] = "1px"
        GListBox_108["font"] = ft
        GListBox_108["fg"] = "#000000"
        GListBox_108["justify"] = "left"
        GListBox_108.place(x=80, y=80, width=163, height=580)

        GLabel_868 = tk.Label(fit_frame)
        GLabel_868["font"] = ft
        GLabel_868["fg"] = "#333333"
        GLabel_868["justify"] = "center"
        GLabel_868["text"] = "File list"
        GLabel_868.place(x=80, y=30, width=160, height=40)

        GButton_768 = tk.Button(fit_frame)
        GButton_768["bg"] = "#f0f0f0"
        GButton_768["font"] = ft
        GButton_768["fg"] = "#000000"
        GButton_768["justify"] = "center"
        GButton_768["text"] = "Select file"
        GButton_768.place(x=80, y=690, width=150, height=30)
        GButton_768["command"] = self.GButton_768_command

        fig, ax = plt.subplots()

        canvas = FigureCanvasTkAgg(fig, master=fit_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=1030, y=80, width=548, height=472)

        GLabel_662 = tk.Label(fit_frame)
        GLabel_662["font"] = ft
        GLabel_662["fg"] = "#333333"
        GLabel_662["justify"] = "center"
        GLabel_662["text"] = "Fit p-values"
        GLabel_662.place(x=320, y=30, width=433, height=40)

        GButton_290 = tk.Button(fit_frame)
        GButton_290["bg"] = "#f0f0f0"
        GButton_290["font"] = ft
        GButton_290["fg"] = "#000000"
        GButton_290["justify"] = "center"
        GButton_290["text"] = "Help"
        GButton_290.place(x=80, y=880, width=150, height=30)
        GButton_290["command"] = self.GButton_290_command

        GListBox_753 = tk.Listbox(fit_frame)
        GListBox_753["bg"] = "#ffffff"
        GListBox_753["borderwidth"] = "1px"
        GListBox_753["font"] = ft
        GListBox_753["fg"] = "#333333"
        GListBox_753["justify"] = "center"
        GListBox_753.place(x=1030, y=710, width=558, height=204)

        dsc_functions = ["Single Gaussian", "Double Gaussian", "Triple Gaussian"]
        self.fit_selected_function = tk.StringVar(fit_frame)
        self.fit_selected_function.set(dsc_functions[1])

        info = self.fit_entries_info

        for i in range(1, 13):
            self.fit_entries.append(self.create_entry(fit_frame, '1px', ft, 'grey', 'center',
                                                      info[i]['x'], info[i]['y'], info[i]['width'], info[i]['height'],
                                                      info[i]['text']))

        # Crear el menú desplegable
        GButton_337 = tk.OptionMenu(fit_frame, self.fit_selected_function, *dsc_functions,
                                    command=self.toggle_entry_visibility)
        GButton_337.place(x=330, y=100, width=150, height=30)

        GLabel_662 = tk.Label(fit_frame)
        GLabel_662["font"] = ft
        GLabel_662["fg"] = "#333333"
        GLabel_662["justify"] = "center"
        GLabel_662["text"] = "Fit parameters"
        GLabel_662.place(x=320, y=570, width=433, height=40)

        low_interval = tk.Entry(fit_frame)
        low_interval["borderwidth"] = '1px'
        low_interval["font"] = ft
        low_interval["fg"] = 'grey'
        low_interval["justify"] = 'center'
        low_interval.insert(0, 'Interval T1 (~200)')
        low_interval.bind("<FocusIn>", lambda event, entry=low_interval: self.on_entry_click(event, entry))
        low_interval.bind("<FocusOut>", lambda event, entry=low_interval,
                                               text='Interval T1 (~200)': self.on_entry_leave(event, entry, text))
        low_interval.place(x=320, y=650, width=160, height=30)

        high_interval = tk.Entry(fit_frame)
        high_interval["borderwidth"] = '1px'
        high_interval["font"] = ft
        high_interval["fg"] = 'grey'
        high_interval["justify"] = 'center'
        high_interval.insert(0, 'Interval T2 (~500)')
        high_interval.bind("<FocusIn>", lambda event, entry=high_interval: self.on_entry_click(event, entry))
        high_interval.bind("<FocusOut>", lambda event, entry=high_interval,
                                                text='Interval T2 (~500)': self.on_entry_leave(event, entry, text))
        high_interval.place(x=590, y=650, width=160, height=30)

        max_tries = tk.Entry(fit_frame)
        max_tries["borderwidth"] = '1px'
        max_tries["font"] = ft
        max_tries["fg"] = 'grey'
        max_tries["justify"] = 'center'
        max_tries.insert(0, 'Max tries (~500-2000)')
        max_tries.bind("<FocusIn>", lambda event, entry=max_tries: self.on_entry_click(event, entry))
        max_tries.bind("<FocusOut>", lambda event, entry=max_tries,
                                               text='Max tries (~500-2000)': self.on_entry_leave(event, entry, text))
        max_tries.place(x=320, y=710, width=160, height=30)

        fit_calculate_button = tk.Button(fit_frame)
        fit_calculate_button["bg"] = "#f0f0f0"
        fit_calculate_button["font"] = ft
        fit_calculate_button["fg"] = "#000000"
        fit_calculate_button["justify"] = "center"
        fit_calculate_button["text"] = "Calculate"
        fit_calculate_button.place(x=450, y=770, width=160, height=30)
        fit_calculate_button["command"] = self.GButton_290_command

        return fit_frame

    def results_body(self):
        width = 1770
        height = 1030

        results_frame = tk.Frame(self.body, bg=MAIN_BODY_COLOR)
        results_frame.config(width=width, height=height)

        ft = font.Font(family='FontAwesome', size=12)

        GListBox_108 = tk.Listbox(results_frame)
        GListBox_108["bg"] = "#e0d7d7"
        GListBox_108["borderwidth"] = "1px"
        GListBox_108["font"] = ft
        GListBox_108["fg"] = "#000000"
        GListBox_108["justify"] = "left"
        GListBox_108.place(x=80, y=80, width=163, height=580)

        GLabel_868 = tk.Label(results_frame)
        GLabel_868["font"] = ft
        GLabel_868["fg"] = "#333333"
        GLabel_868["justify"] = "center"
        GLabel_868["text"] = "File list"
        GLabel_868.place(x=80, y=30, width=160, height=40)

        GButton_768 = tk.Button(results_frame)
        GButton_768["bg"] = "#f0f0f0"
        GButton_768["font"] = ft
        GButton_768["fg"] = "#000000"
        GButton_768["justify"] = "center"
        GButton_768["text"] = "Select file"
        GButton_768.place(x=80, y=690, width=150, height=30)
        GButton_768["command"] = self.GButton_768_command

        results_unselect_button = tk.Button(results_frame)
        results_unselect_button["bg"] = "#f0f0f0"
        results_unselect_button["font"] = ft
        results_unselect_button["fg"] = "#000000"
        results_unselect_button["justify"] = "center"
        results_unselect_button["text"] = "Unselect file"
        results_unselect_button.place(x=80, y=740, width=150, height=30)
        results_unselect_button["command"] = self.GButton_768_command

        GListBox_363 = tk.Listbox(results_frame)
        GListBox_363["bg"] = "#e0d7d7"
        GListBox_363["borderwidth"] = "1px"
        GListBox_363["font"] = ft
        GListBox_363["fg"] = "#333333"
        GListBox_363["justify"] = "left"
        GListBox_363.place(x=320, y=80, width=700, height=834)


        GLabel_662 = tk.Label(results_frame)
        GLabel_662["font"] = ft
        GLabel_662["fg"] = "#333333"
        GLabel_662["justify"] = "center"
        GLabel_662["text"] = "Results"
        GLabel_662.place(x=320, y=30, width=700, height=40)

        GButton_290 = tk.Button(results_frame)
        GButton_290["bg"] = "#f0f0f0"
        GButton_290["font"] = ft
        GButton_290["fg"] = "#000000"
        GButton_290["justify"] = "center"
        GButton_290["text"] = "Help"
        GButton_290.place(x=80, y=880, width=150, height=30)
        GButton_290["command"] = self.GButton_290_command

        GListBox_753 = tk.Listbox(results_frame)
        GListBox_753["bg"] = "#ffffff"
        GListBox_753["borderwidth"] = "1px"
        GListBox_753["font"] = ft
        GListBox_753["fg"] = "#333333"
        GListBox_753["justify"] = "center"
        GListBox_753.place(x=1100, y=584, width=510, height=330)

        GLabel_256 = tk.Label(results_frame)
        GLabel_256["font"] = ft
        GLabel_256["fg"] = "#333333"
        GLabel_256["justify"] = "center"
        GLabel_256["text"] = "Export results"
        GLabel_256.place(x=1100, y=30, width=510, height=40)


        table = ["Proc data", "Calc results", "Fit results"]
        selected_table = tk.StringVar(results_frame)
        selected_table.set(table[0])

        # Función para cambiar el idioma seleccionado
        def change_table(*args):
            print(f"Selected table: {selected_table.get()}")

        # Crear el menú desplegable
        GButton_336 = tk.OptionMenu(results_frame, selected_table, *table, command=change_table())
        GButton_336.place(x=1100, y=100, width=150, height=30)


        file_type = ["Excel file", "CSV file", "LaTeX table"]
        selected_type = tk.StringVar(results_frame)
        selected_type.set(file_type[0])

        # Función para cambiar el idioma seleccionado
        def change_type(*args):
            print(f"Selected type: {selected_type.get()}")

        # Crear el menú desplegable
        GButton_337 = tk.OptionMenu(results_frame, selected_type, *file_type, command=change_type())
        GButton_337.place(x=1290, y=100, width=150, height=30)

        GButton_291 = tk.Button(results_frame)
        GButton_291["bg"] = "#f0f0f0"
        GButton_291["font"] = ft
        GButton_291["fg"] = "#000000"
        GButton_291["justify"] = "center"
        GButton_291["text"] = "Export"
        GButton_291.place(x=1290, y=150, width=150, height=30)
        GButton_291["command"] = self.GButton_290_command


        return results_frame

    def log_message_dashboard(self, message):
        self.dashboard_console.insert(tk.END, f"{message}\n")
        self.dashboard_console.see(tk.END)  # Desplazarse automáticamente al final del texto

    def on_entry_click(self, event, entry):
        entry.delete(0, tk.END)
        entry.config(fg='black')  # Cambia el color del texto cuando se escribe

    def on_entry_leave(self, event, entry, text):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg='grey')  # Restaura el color del texto predeterminado

    def toggle_entry_visibility(self, event=None):
        selection = self.fit_selected_function.get()
        if selection == "Single Gaussian":
            self.show_entries(4)
        elif selection == "Double Gaussian":
            self.show_entries(8)
        else:
            self.show_entries(12)

    def show_entries(self, num_entries):
        info = self.fit_entries_info
        for i, entry in enumerate(self.fit_entries):
            if i < num_entries:
                entry.place(x=info[i + 1]['x'], y=info[i + 1]['y'], width=info[i + 1]['width'],
                            height=info[i + 1]['height'])
            else:
                entry.place_forget()

    def GButton_290_command(self):
        print("command")
        return 1

    def GButton_336_command(self):
        print("command")

    def GButton_645_command(self):
        print("command")

    def GButton_780_command(self):
        print("command")

    def GButton_205_command(self):
        print("command")

    def GButton_547_command(self):
        print("command")

    def GButton_490_command(self):
        print("command")

    def GButton_64_command(self):
        print("command")

    def GButton_542_command(self):
        print("command")

    def GButton_651_command(self):
        print("command")

    def GButton_813_command(self):
        print("command")

    def GButton_754_command(self):
        print("command")

    def select_file(self):

        pass

    def realize_calc(self):

        pass

    def graphic_calc(self):

        pass

    def calculate_with_parameters(self, param_entries):
        # Lógica para tomar los valores ingresados por el usuario y realizar los cálculos necesarios
        parameters = [entry.get() for entry in param_entries]  # Obtener los valores ingresados
        # Realizar cálculos con los parámetros proporcionados
        # Puedes utilizar estos valores para realizar las operaciones necesarias
        pass

    def top_bar_controls(self):

        font_awesome = font.Font(family='FontAwesome', size=12)

        self.titleLabel = tk.Label(self.top_bar, text='DSC-TGA Analyzer')
        self.titleLabel.config(fg="#fff", font=(
            "Roboto", 15), bg=TOP_BAR_COLOR, pady=10, width=16)
        self.titleLabel.pack(side=tk.LEFT)

        self.buttonSideMenu = tk.Button(self.top_bar, text='Menu', font=font_awesome,
                                        command=self.toggle_panel, bd=0, bg=TOP_BAR_COLOR, fg="white")
        self.buttonSideMenu.pack(side=tk.LEFT)

        self.titleLabel = tk.Label(
            self.top_bar, text='daniel.sieiro@rai.usc.es')
        self.titleLabel.config(fg="#fff", font=(
            "Roboto", 10), bg=TOP_BAR_COLOR, padx=10, width=20)
        self.titleLabel.pack(side=tk.RIGHT)

    def side_menu_controls(self):

        width_menu = 20
        height_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        self.profileLabel = tk.Label(
            self.side_menu, image=self.profile, bg=SIDE_MENU_COLOR)
        self.profileLabel.pack(side=tk.TOP, pady=10)

        self.buttonDashBoard = tk.Button(self.side_menu)
        self.buttonCalculator = tk.Button(self.side_menu)
        self.buttonGraph = tk.Button(self.side_menu)
        self.buttonFit = tk.Button(self.side_menu)
        self.buttonResults = tk.Button(self.side_menu)
        # 117 uf013(flecha) uf210)(teclado)
        buttons_info = [
            ("Dashboard", "\uf210", self.buttonDashBoard),
            ("Calculator", "\uf007", self.buttonCalculator),
            ("Graphics", "\uf128", self.buttonGraph),
            ("Fit", "\uf120", self.buttonFit),
            ("Results", "\uf133", self.buttonResults)
        ]

        for text, icon, button in buttons_info:
            self.menu_button_config(button, text, icon, font_awesome, width_menu, height_menu)

        self.buttonDashBoard.config(command=lambda: self.show_body('Dashboard'))
        self.buttonCalculator.config(command=lambda: self.show_body('Calculator'))
        self.buttonGraph.config(command=lambda: self.show_body('Graphics'))
        self.buttonFit.config(command=lambda: self.show_body('Fit'))
        self.buttonResults.config(command=lambda: self.show_body('Results'))

    def menu_button_config(self, button, text, icon, font_awesome, width_menu, height_menu):

        button.config(text=f"  {icon}  {text}", anchor="w", font=font_awesome,
                      bd=0, bg=SIDE_MENU_COLOR, fg="white", width=width_menu, height=height_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):

        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):

        button.config(bg=HOVER_MENU_CURSOR_COLOR, fg="white")

    def on_leave(self, event, button):

        button.config(bg=SIDE_MENU_COLOR, fg="white")

    def toggle_panel(self):

        if self.side_menu.winfo_ismapped():
            self.side_menu.pack_forget()
        else:
            self.side_menu.pack(side=tk.LEFT, fill='y')

    def toggle_text(self):

        if self.side_menu.winfo_ismapped():
            return '\uf013'
        else:
            return fa.icons['envelope']

    def show_help(self):
        # Lógica para mostrar la ayuda
        pass

    def show_body(self, section_name):
        # Diccionario que contiene los nombres de las secciones y sus métodos correspondientes
        for section, widgets in self.sections_widgets.items():
            if section == section_name:
                if widgets is None:
                    # Si los widgets de esta sección no existen, crearlos y almacenarlos
                    self.sections_widgets[section] = self.create_section_widgets(section)
                widgets = self.sections_widgets[section]
                if section_name!='Graphics':
                    self.file_listbox.place(x=80, y=80, width=163, height=580, in_=self.sections_widgets[section])
                widgets.pack(fill=tk.BOTH, expand=True)
            elif widgets is not None:
                widgets.pack_forget()

    def add_file(self, files_listbox):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx")])
        keys_list = list(self.loaded_files.keys())
        if file_path:
            self.dashboard_console.config(state='normal')
            if file_path not in self.file_paths:
                file_name = os.path.basename(file_path)
                self.log_message_dashboard(f'Adding {file_name} from {file_path}...')
                files_listbox.insert(tk.END, file_name)
                self.loaded_files[file_name] = (pd.read_excel(file_path), file_path)
                self.ta_objects.append(ThermalAnalysis(self.loaded_files[file_name][0]))
                self.log_message_dashboard('File added as pandas.DataFrame.')
                self.file_paths.append(file_path)
            else:
                self.log_message_dashboard('This file is already added')
            self.dashboard_console.config(state='disabled')

    def delete_file(self, files_listbox):
        selected = files_listbox.curselection()
        keys_list = list(self.loaded_files.keys())
        self.dashboard_console.config(state='normal')
        for i in selected:
            self.log_message_dashboard(f'Removing {keys_list[i]}...')
            files_listbox.delete(i)
            del self.loaded_files[keys_list[i]]
            del self.file_paths[i]
            del self.ta_objects[i]
            self.log_message_dashboard(f'{keys_list[i]} removed.')
        self.dashboard_console.config(state='disabled')

    def show_file_info(self, files_listbox, files_infobox, fig, ax, ax2, canvas):
        self.dashboard_console.config(state='normal')
        files_infobox.config(state='normal')
        selected = files_listbox.curselection()
        for i in selected:
            ax.clear()
            ax2.clear()
            canvas.draw()
            key = list(self.loaded_files.keys())[i]
            files_infobox.delete("1.0", tk.END)  # Borra el contenido actual
            files_infobox.insert(tk.END, self.loaded_files[key][0][['Ts','HF/M','% mass']].to_string())
            ax.set_xlabel('Temperature / °C')
            ax.set_ylabel('Heat Flow / J $\cdot$ $g^{-1}$')
            ax2.set_ylabel('% Mass')
            data = self.ta_objects[i].get_data()
            line1, = ax.plot(data['Ts'], data['HF/M'],'k--',label='DSC')
            line2, = ax2.plot(data['Ts'], data['% mass'], 'k-', label='TGA')
            lines = [line1, line2]
            ax.legend(lines, [line.get_label() for line in lines], loc='upper right')
            ax.set_xlim(data['Ts'].min(), data['Ts'].max())
            ax.set_ylim(data['HF/M'].min()*1.1, data['HF/M'].max()*1.4)
            ax2.set_ylim(data['% mass'].min(), data['% mass'].max())
            canvas.draw()
        self.dashboard_console.config(state='disabled')
        files_infobox.config(state='disabled')
        pass

    def create_section_widgets(self, section_name):
        if section_name == 'Dashboard':
            return self.dashboard_body()
        elif section_name == 'Calculator':
            return self.calculator_body()
        elif section_name == 'Graphics':
            return self.graphics_body()
        elif section_name == 'Fit':
            return self.fit_body()
        elif section_name == 'Results':
            return self.results_body()


def calculate_values():
    pass


def plot_graph():
    # Lógica para crear y mostrar la gráfica
    data = [1, 2, 3, 4, 5]  # Ejemplo de datos para la gráfica
    plt.plot(data)
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Gráfica')
    plt.show()
