from tkinter import ttk

import tkinter as tk

from SleepModel import SleepModel


class SleepFrame:
    def __init__(self, parent, app, is_premium=False):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.is_premium = is_premium
        self.sleep_schedule = []
        self.current_day = 1

        self.bed_combo = None
        self.wake_combo = None
        self.day_label = None
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="nsew")

        for i in range(8):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.frame.grid_columnconfigure(i, weight=1)

        self.setup_ui()

    def save_data(self):
        try:
            self.save_current_day()
            valid_days = [day for day in self.sleep_schedule if day[0] and day[1]]

            if len(valid_days) < 1:
                self.status_label.config(text="Ошибка: Введите данные хотя бы за 1 день", fg='red')
                return

            sleep_model = SleepModel()
            results = sleep_model.periodic_stress(valid_days)

            self.status_label.config(
                text=f"Данные сохранены! Заполнено дней: {len(valid_days)}",
                fg='green'
            )

            return results

        except Exception as e:
            self.status_label.config(text=f"Ошибка сохранения: {str(e)}", fg='red')

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.frame,
            text="Анализ качества сна",
            font=('Arial', 24, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=5, pady=(10, 5), sticky='ew')

        info_label = tk.Label(
            self.frame,
            text="Введите данные о времени сна",
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

        time_options = [f"{h:02d}:{m:02d}" for h in range(0, 24) for m in [0, 10, 20, 30, 40, 50]]

        time_container = tk.Frame(self.frame, bg='lightblue')
        time_container.grid(row=3, column=0, columnspan=5, pady=15, sticky='ew')

        for i in range(3):
            time_container.grid_columnconfigure(i, weight=1)

        bed_frame = tk.Frame(time_container, bg='lightblue')
        bed_frame.grid(row=0, column=0, sticky='e', padx=5)
        bed_frame.grid_columnconfigure(0, weight=1)
        bed_frame.grid_columnconfigure(1, weight=0)

        bed_label = tk.Label(
            bed_frame,
            text="Время отхода ко сну:",
            font=('Arial', 14, 'bold'),
            bg='lightblue',
            fg='black'
        )
        bed_label.grid(row=0, column=0, sticky='e', padx=(0, 6))

        self.bed_combo = ttk.Combobox(
            bed_frame,
            values=time_options,
            width=10,
            state="readonly",
            font=('Arial', 14)
        )
        self.bed_combo.set("23:00")
        self.bed_combo.grid(row=0, column=1, sticky='w')


        wake_frame = tk.Frame(time_container, bg='lightblue')
        wake_frame.grid(row=0, column=2, sticky='w', padx=5)
        wake_frame.grid_columnconfigure(0, weight=1)
        wake_frame.grid_columnconfigure(1, weight=0)

        wake_label = tk.Label(
            wake_frame,
            text="Время подъема:",
            font=('Arial', 14, 'bold'),
            bg='lightblue',
            fg='black'
        )
        wake_label.grid(row=0, column=0, sticky='e', padx=(0, 6))

        self.wake_combo = ttk.Combobox(
            wake_frame,
            values=time_options,
            width=10,
            state="readonly",
            font=('Arial', 14)
        )
        self.wake_combo.set("07:00")
        self.wake_combo.grid(row=0, column=1, sticky='w')

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
        back_button.grid(row=5, column=0, columnspan=5, pady=10, sticky='s')

        self.update_day_display()
        self.update_navigation_buttons()

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
        bed_time = self.bed_combo.get()
        wake_time = self.wake_combo.get()

        if bed_time and wake_time:
            while len(self.sleep_schedule) < self.current_day:
                self.sleep_schedule.append(("23:00", "07:00"))

            self.sleep_schedule[self.current_day - 1] = (bed_time, wake_time)

    def update_day_display(self):
        self.day_label.config(text=f"День {self.current_day}")

        if len(self.sleep_schedule) >= self.current_day:
            bed_time, wake_time = self.sleep_schedule[self.current_day - 1]
            self.bed_combo.set(bed_time)
            self.wake_combo.set(wake_time)
        else:
            self.bed_combo.set("23:00")
            self.wake_combo.set("07:00")

    def update_navigation_buttons(self):
        if self.is_premium:
            self.prev_button.config(state='normal' if self.current_day > 1 else 'disabled')
            self.next_button.config(state='normal')



    def go_back(self):
        self.app.show_main_menu()