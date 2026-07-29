from tkinter import ttk

import tkinter as tk

from Emotional_Model import EmotionModel


class EmotionFrame:
    def __init__(self, parent, app, is_premium=False):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.is_premium = is_premium
        self.emotion_data = []
        self.current_day = 1
        self.sadness_var = tk.StringVar(value="5")
        self.anxiety_var = tk.StringVar(value="5")
        self.anger_var = tk.StringVar(value="5")
        self.joy_var = tk.StringVar(value="5")
        self.social_hours_var = tk.StringVar(value="2.0")
        self.isolation_hours_var = tk.StringVar(value="2.0")

        self.day_label = None
        self.status_label = None
        self.prev_button = None
        self.next_button = None

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="nsew")

        for i in range(12):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.frame.grid_columnconfigure(i, weight=1)

        self.setup_ui()

    def save_data(self):
        try:
            self.save_current_day()

            valid_days = [day for day in self.emotion_data if any(day.values())]

            if len(valid_days) < 1:
                self.status_label.config(text="Ошибка: Введите данные хотя бы за 1 день", fg='red')
                return

            emotion_model = EmotionModel()
            emotion_score = emotion_model.periodic_stress(valid_days)

            self.last_calculated_score = emotion_score

            day_count = len(valid_days)
            self.status_label.config(
                text=f"Данные сохранены! Заполнено дней: {day_count}",
                fg='green'
            )

            return emotion_score

        except ValueError as e:
            self.status_label.config(text=f"Ошибка: {str(e)}", fg='red')
        except Exception as e:
            self.status_label.config(text=f"Ошибка сохранения: {str(e)}", fg='red')

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.frame,
            text="Анализ эмоционального состояния",
            font=('Arial', 24, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=5, pady=(10, 5), sticky='ew')

        info_label = tk.Label(
            self.frame,
            text="Введите данные об эмоциях за день",
            font=('Arial', 16),
            bg='lightblue',
            fg='black'
        )
        info_label.grid(row=1, column=0, columnspan=5, pady=(0, 10), sticky='ew')

        self.day_label = tk.Label(
            self.frame,
            text=f"День {self.current_day}",
            font=('Arial', 18, 'bold'),
            bg='lightblue',
            fg='black'
        )
        self.day_label.grid(row=2, column=0, columnspan=5, pady=10, sticky='ew')

        form_container = tk.Frame(self.frame, bg='lightblue')
        form_container.grid(row=3, column=0, columnspan=5, pady=10, sticky='nsew')

        for i in range(8):
            form_container.grid_rowconfigure(i, weight=1)
        for i in range(3):
            form_container.grid_columnconfigure(i, weight=1)

        row_counter = 0
        col = 1

        emotion_options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.create_combobox_widget(form_container, row_counter, col, "Грусть:", self.sadness_var, emotion_options)
        row_counter += 1

        self.create_combobox_widget(form_container, row_counter, col, "Тревога:", self.anxiety_var, emotion_options)
        row_counter += 1

        self.create_combobox_widget(form_container, row_counter, col, "Гнев:", self.anger_var, emotion_options)
        row_counter += 1

        self.create_combobox_widget(form_container, row_counter, col, "Радость:", self.joy_var, emotion_options)
        row_counter += 1

        social_options = ['0.0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0', '9.5', '10.0', '10.5', '11.0', '11.5', '12.0', '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0', '16.5', '17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0', '20.5', '21.0', '21.5', '22.0', '22.5', '23.0', '23.5', '24.0']
        self.create_combobox_widget(form_container, row_counter, col, "Часы общения:", self.social_hours_var, social_options)
        row_counter += 1

        self.create_combobox_widget(form_container, row_counter, col, "Часы одиночества:", self.isolation_hours_var, social_options)
        row_counter += 1

        if self.is_premium:
            nav_frame = tk.Frame(self.frame, bg='lightblue')
            nav_frame.grid(row=4, column=0, columnspan=5, pady=10, sticky='ew')

            for i in range(5):
                nav_frame.grid_columnconfigure(i, weight=1)

            self.prev_button = tk.Button(
                nav_frame,
                text="← Предыдущий день",
                font=('Arial', 12),
                bg='grey',
                fg='white',
                width=18,
                height=1,
                command=self.previous_day,
                state='disabled'
            )
            self.prev_button.grid(row=0, column=1, padx=5, sticky='e')

            self.next_button = tk.Button(
                nav_frame,
                text="Следующий день →",
                font=('Arial', 12),
                bg='grey',
                fg='white',
                width=18,
                height=1,
                command=self.next_day
            )
            self.next_button.grid(row=0, column=3, padx=5, sticky='w')

        save_button = tk.Button(
            self.frame,
            text="Сохранить данные",
            font=('Arial', 14, 'bold'),
            bg='green',
            fg='white',
            width=20,
            height=2,
            command=self.save_data
        )
        save_button.grid(row=5, column=0, columnspan=5, pady=10, sticky='n')

        self.status_label = tk.Label(
            self.frame,
            text="",
            font=('Arial', 12),
            bg='lightblue',
            fg='green'
        )
        self.status_label.grid(row=6, column=0, columnspan=5, pady=5, sticky='n')

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

        self.update_day_display()
        self.update_navigation_buttons()

    def create_combobox_widget(self, parent, row, col, label_text, variable, values):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        label = tk.Label(container, text=label_text, font=('Arial', 14, 'bold'), bg='lightblue', fg='black')
        label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        combobox = ttk.Combobox(
            container,
            values=values,
            textvariable=variable,
            width=10,
            font=('Arial', 14, 'bold'),
            state='readonly'
        )
        combobox.grid(row=0, column=1, sticky='w', padx=5)
        return combobox

    def previous_day(self):
        if self.current_day > 1:
            self.save_current_day()
            self.current_day -= 1
            self.update_day_display()
            self.update_navigation_buttons()

    def next_day(self):
        self.save_current_day()
        self.current_day += 1
        self.update_day_display()
        self.update_navigation_buttons()

    def save_current_day(self):
        day_data = {
            'sadness': int(self.sadness_var.get()),
            'anxiety': int(self.anxiety_var.get()),
            'anger': int(self.anger_var.get()),
            'joy': int(self.joy_var.get()),
            'social_hours': float(self.social_hours_var.get()),
            'isolation_hours': float(self.isolation_hours_var.get())
        }

        while len(self.emotion_data) < self.current_day:
            self.emotion_data.append({
                'sadness': 5,
                'anxiety': 5,
                'anger': 5,
                'joy': 5,
                'social_hours': 2.0,
                'isolation_hours': 2.0
            })

        self.emotion_data[self.current_day - 1] = day_data

    def update_day_display(self):
        self.day_label.config(text=f"День {self.current_day}")

        if len(self.emotion_data) >= self.current_day:
            day_data = self.emotion_data[self.current_day - 1]
            self.sadness_var.set(str(day_data['sadness']))
            self.anxiety_var.set(str(day_data['anxiety']))
            self.anger_var.set(str(day_data['anger']))
            self.joy_var.set(str(day_data['joy']))
            self.social_hours_var.set(str(day_data['social_hours']))
            self.isolation_hours_var.set(str(day_data['isolation_hours']))

    def update_navigation_buttons(self):
        if self.is_premium:
            self.prev_button.config(state='normal' if self.current_day > 1 else 'disabled')
            self.next_button.config(state='normal')

    def go_back(self):
        self.app.show_main_menu()