import tkinter as tk

from Activity_Res import ActivityResultFrame
from Emotion_Res import EmotionResultFrame
from Food_Res import FoodResultFrame
from Overall import OverallResultFrame
from Sleep_Res import SleepResultFrame


class ResultFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(12):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.frame.grid_columnconfigure(i, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Результаты анализа стресса",
            font=('Arial', 24, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=5, pady=(20, 10), sticky='ew')

        buttons_container = tk.Frame(self.frame, bg='lightblue')
        buttons_container.grid(row=1, column=0, columnspan=5, rowspan=2, pady=10, sticky='nsew')

        for i in range(2):
            buttons_container.grid_rowconfigure(i, weight=1)
        for i in range(2):
            buttons_container.grid_columnconfigure(i, weight=1)

        sleep_button = tk.Button(
            buttons_container,
            text="Сон",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.show_sleep_result
        )
        sleep_button.grid(row=0, column=0, pady=10, padx=10, sticky='e')

        food_button = tk.Button(
            buttons_container,
            text="Питание",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.show_food_result
        )
        food_button.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        activity_button = tk.Button(
            buttons_container,
            text="Активность",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.show_activity_result
        )
        activity_button.grid(row=1, column=0, pady=10, padx=10, sticky='e')

        emotions_button = tk.Button(
            buttons_container,
            text="Эмоции",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.show_emotion_result
        )
        emotions_button.grid(row=1, column=1, pady=10, padx=10, sticky='w')

        if self.app.is_premium:
            overall_button = tk.Button(
                self.frame,
                text="Общий результат",
                font=('Arial', 14, 'bold'),
                bg='orange',
                fg='white',
                width=25,
                height=2,
                command=self.show_overall_result
            )
            overall_button.grid(row=5, column=0, columnspan=5, pady=20, sticky='n')
        else:
            premium_label = tk.Label(
                self.frame,
                text="Общий результат доступен только в премиум-режиме",
                font=('Arial', 14, 'bold'),
                bg='lightblue',
                fg='black'
            )
            premium_label.grid(row=5, column=0, columnspan=5, pady=10, sticky='n')

            activate_button = tk.Button(
                self.frame,
                text="Перейти в премиум-режим",
                font=('Arial', 14, 'bold'),
                bg='orange',
                fg='white',
                width=25,
                height=2,
                command=self.show_activation_frame
            )
            activate_button.grid(row=6, column=0, columnspan=5, pady=10, sticky='n')

        back_button = tk.Button(
            self.frame,
            text="Назад в главное меню",
            font=('Arial', 12),
            bg='grey',
            fg='white',
            width=18,
            height=1,
            command=self.go_back
        )
        back_button.grid(row=7, column=0, columnspan=5, pady=10, sticky='s')

    def show_activation_frame(self):
        self.app.show_activation_window()

    def show_sleep_result(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
        sleep_result_frame = SleepResultFrame(self.app.root, self.app)
        sleep_result_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_food_result(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
        food_result_frame = FoodResultFrame(self.app.root, self.app)
        food_result_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_activity_result(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
        activity_result_frame = ActivityResultFrame(self.app.root, self.app)
        activity_result_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_emotion_result(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
        emotion_result_frame = EmotionResultFrame(self.app.root, self.app)
        emotion_result_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_overall_result(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
        overall_result_frame = OverallResultFrame(self.app.root, self.app)
        overall_result_frame.frame.grid(row=0, column=0, sticky="nsew")

    def go_back(self):
        self.app.show_main_menu()