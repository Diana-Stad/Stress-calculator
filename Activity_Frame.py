from tkinter import ttk

import tkinter as tk

from Activity_Model import ActivityModel


class ActivityFrame:
    def __init__(self, parent, app, is_premium=False):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.is_premium = is_premium
        self.activity_data = []
        self.current_day = 1

        self.work_hours_var = tk.StringVar(value='8.0')
        self.work_type_var = tk.StringVar(value='office')
        self.work_stress_var = tk.StringVar(value='5')
        self.work_night_var = tk.BooleanVar(value=False)
        self.work_start_hour_var = tk.StringVar(value='22')
        self.exercise_var = tk.StringVar(value='none')
        self.exercise_duration_var = tk.StringVar(value='0')

        self.day_label = None
        self.status_label = None
        self.prev_button = None
        self.next_button = None
        self.duration_label = None
        self.exercise_duration_combobox = None

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

            valid_days = [day for day in self.activity_data if any(day.values())]

            if len(valid_days) < 1:
                self.status_label.config(text="Ошибка: Введите данные хотя бы за 1 день", fg='red')
                return

            activity_model = ActivityModel()
            activity_score = activity_model.periodic_stress(valid_days)

            day_count = len(valid_days)
            self.status_label.config(
                text=f"Данные сохранены! Заполнено дней: {day_count}",
                fg='green'
            )

            return activity_score

        except ValueError as e:
            self.status_label.config(text=f"Ошибка: {str(e)}", fg='red')
        except Exception as e:
            self.status_label.config(text=f"Ошибка сохранения: {str(e)}", fg='red')

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.frame,
            text="Анализ активности",
            font=('Arial', 24, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=5, pady=(10, 5), sticky='ew')

        info_label = tk.Label(
            self.frame,
            text="Введите данные об активности за день",
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

        for i in range(9):
            form_container.grid_rowconfigure(i, weight=1)
        for i in range(3):
            form_container.grid_columnconfigure(i, weight=1)

        row_counter = 0
        col = 1

        work_hours_options = ['0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0',
                              '6.5', '7.0', '7.5', '8.0', '8.5', '9.0', '9.5', '10.0', '10.5', '11.0', '11.5', '12.0',
                              '12.5', '13.0', '13.5', '14.0', '14.5', '15.0', '15.5', '16.0']
        self.create_combobox_widget(form_container, row_counter, col, "Часы работы:", self.work_hours_var,
                                    work_hours_options)
        row_counter += 1

        self.create_work_type_widget(form_container, row_counter, col, "Тип работы:", self.work_type_var)
        row_counter += 1

        work_stress_options = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.create_combobox_widget(form_container, row_counter, col, "Стресс работы (0-10):", self.work_stress_var,
                                    work_stress_options)
        row_counter += 1

        self.create_exercise_widget(form_container, row_counter, col, "Тренировка:", self.exercise_var)
        row_counter += 1

        self.create_exercise_duration_widget(form_container, row_counter, col)
        row_counter += 1

        night_container = tk.Frame(form_container, bg='lightblue')
        night_container.grid(row=row_counter, column=0, columnspan=3, pady=10, sticky='ew')

        for i in range(8):
            night_container.grid_columnconfigure(i, weight=1)

        def update_night_shift_state():
            if self.work_night_var.get():
                start_combobox.config(state='readonly')
                start_label.config(fg='black')
            else:
                start_combobox.config(state='disabled')
                start_label.config(fg='gray')

        night_cb = tk.Checkbutton(night_container, text="Ночная смена",
                                  variable=self.work_night_var, bg='lightblue', fg='black',
                                  font=('Arial', 14, 'bold'),
                                  command=update_night_shift_state)
        night_cb.grid(row=1, column=3, padx=10, sticky='w')

        start_label = tk.Label(night_container, text="Начало смены:", font=('Arial', 14, 'bold'), bg='lightblue',
                               fg='gray')
        start_label.grid(row=1, column=4, padx=10, sticky='e')

        start_hours_options = [str(i) for i in range(21,24)]
        start_combobox = ttk.Combobox(
            night_container,
            values=start_hours_options,
            textvariable=self.work_start_hour_var,
            width=5,
            font=('Arial', 14, 'bold'),
            state='disabled'
        )
        start_combobox.set('22')
        start_combobox.grid(row=1, column=5, padx=10, sticky='w')

        update_night_shift_state()

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
        save_button.grid(row=6, column=0, columnspan=5, pady=10, sticky='n')

        self.status_label = tk.Label(
            self.frame,
            text="",
            font=('Arial', 12),
            bg='lightblue',
            fg='green'
        )
        self.status_label.grid(row=7, column=0, columnspan=5, pady=5, sticky='n')

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
        back_button.grid(row=8, column=0, columnspan=5, pady=10, sticky='s')

        self.update_day_display()
        self.update_navigation_buttons()
        self.update_exercise_duration_state()

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

    def create_work_type_widget(self, parent, row, col, label_text, variable):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        label = tk.Label(container, text=label_text, font=('Arial', 14, 'bold'), bg='lightblue', fg='black')
        label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        type_frame = tk.Frame(container, bg='lightblue')
        type_frame.grid(row=0, column=1, columnspan=2, sticky='w')

        options = [
            ("Офис", 'office'),
            ("Физический", 'physical'),
            ("Смешанный", 'mixed')
        ]

        for i, (text, value) in enumerate(options):
            rb = tk.Radiobutton(type_frame, text=text, variable=variable, value=value,
                                bg='lightblue', fg='black', font=('Arial', 12, 'bold'))
            rb.grid(row=0, column=i, padx=8)
        return type_frame

    def create_exercise_widget(self, parent, row, col, label_text, variable):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        label = tk.Label(container, text=label_text, font=('Arial', 14, 'bold'), bg='lightblue', fg='black')
        label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        exercise_frame = tk.Frame(container, bg='lightblue')
        exercise_frame.grid(row=0, column=1, columnspan=2, sticky='w')

        options = [
            ("Нет", 'none'),
            ("Легкая", 'low'),
            ("Средняя", 'moderate'),
            ("Интенсивная", 'high')
        ]

        for i, (text, value) in enumerate(options):
            rb = tk.Radiobutton(exercise_frame, text=text, variable=variable, value=value,
                                bg='lightblue', fg='black', font=('Arial', 12, 'bold'),
                                command=self.update_exercise_duration_state)
            rb.grid(row=0, column=i, padx=8)
        return container

    def create_exercise_duration_widget(self, parent, row, col):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        self.duration_label = tk.Label(container, text="Длительность (мин):",
                                       font=('Arial', 14, 'bold'), bg='lightblue', fg='gray')
        self.duration_label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        duration_options = ['0', '15', '30', '45', '60', '75', '90', '105', '120', '135', '150', '165', '180']
        self.exercise_duration_combobox = ttk.Combobox(
            container,
            values=duration_options,
            textvariable=self.exercise_duration_var,
            width=10,
            font=('Arial', 14, 'bold'),
            state='disabled'
        )
        self.exercise_duration_combobox.set('0')
        self.exercise_duration_combobox.grid(row=0, column=1, sticky='w', padx=5)

    def update_exercise_duration_state(self):
        if self.exercise_var.get() == 'none':
            self.exercise_duration_combobox.config(state='disabled')
            self.duration_label.config(fg='gray')
            self.exercise_duration_var.set('0')
        else:
            self.exercise_duration_combobox.config(state='readonly')
            self.duration_label.config(fg='black')

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
            'work_hours': float(self.work_hours_var.get()),
            'work_type': self.work_type_var.get(),
            'work_stress': int(self.work_stress_var.get()),
            'work_night': self.work_night_var.get(),
            'work_start_hour': int(self.work_start_hour_var.get()),
            'exercise': self.exercise_var.get(),
            'exercise_duration': int(self.exercise_duration_var.get())
        }

        while len(self.activity_data) < self.current_day:
            self.activity_data.append({
                'work_hours': 8.0,
                'work_type': 'office',
                'work_stress': 5,
                'work_night': False,
                'work_start_hour': 22,
                'exercise': 'none',
                'exercise_duration': 0
            })

        self.activity_data[self.current_day - 1] = day_data

    def update_day_display(self):
        self.day_label.config(text=f"День {self.current_day}")

        if len(self.activity_data) >= self.current_day:
            day_data = self.activity_data[self.current_day - 1]
            self.work_hours_var.set(str(day_data['work_hours']))
            self.work_type_var.set(day_data['work_type'])
            self.work_stress_var.set(str(day_data['work_stress']))
            self.work_night_var.set(day_data['work_night'])
            self.work_start_hour_var.set(str(day_data['work_start_hour']))
            self.exercise_var.set(day_data['exercise'])
            self.exercise_duration_var.set(str(day_data['exercise_duration']))

        self.update_exercise_duration_state()

    def update_navigation_buttons(self):
        if self.is_premium:
            self.prev_button.config(state='normal' if self.current_day > 1 else 'disabled')
            self.next_button.config(state='normal')

    def go_back(self):
        self.app.show_main_menu()
