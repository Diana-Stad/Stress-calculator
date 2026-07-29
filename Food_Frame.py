import tkinter as tk
from Food_Model import FoodModel


class FoodFrame:
    def __init__(self, parent, app, is_premium=False):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.is_premium = is_premium
        self.food_data = []
        self.current_day = 1

        self.quality_var = tk.IntVar(value=1)
        self.snacks_var = tk.IntVar(value=1)
        self.snack_quality_var = tk.IntVar(value=1)
        self.water_var = tk.DoubleVar(value=1.0)
        self.caffeine_var = tk.IntVar(value=1)
        self.alcohol_var = tk.IntVar(value=0)
        self.regularity_var = tk.IntVar(value=1)
        self.fermented_var = tk.BooleanVar()
        self.green_tea_var = tk.BooleanVar()
        self.magnesium_var = tk.BooleanVar()

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

            valid_days = [day for day in self.food_data if any(day.values())]

            if len(valid_days) < 1:
                self.status_label.config(text="Ошибка: Введите данные хотя бы за 1 день", fg='red')
                return
            food_model = FoodModel()
            food_score = food_model.periodic_stress(valid_days)

            self.last_calculated_score = food_score

            day_count = len(valid_days)
            self.status_label.config(
                text=f"Данные сохранены! Заполнено дней: {day_count}",
                fg='green'
            )

            return food_score

        except ValueError as e:
            self.status_label.config(text=f"Ошибка: {str(e)}", fg='red')
        except Exception as e:
            self.status_label.config(text=f"Ошибка сохранения: {str(e)}", fg='red')

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.frame,
            text="Анализ питания",
            font=('Arial', 24, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=5, pady=(10, 5), sticky='ew')

        info_label = tk.Label(
            self.frame,
            text="Введите данные о питании за день",
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
        for i in range(9):
            form_container.grid_columnconfigure(i, weight=1)

        row_counter = 0
        col = 3

        self.create_quality_widget(form_container, row_counter, col, "Качество рациона:", self.quality_var)
        row_counter += 1

        self.create_spinbox_widget(form_container, row_counter, col, "Перекусы:", self.snacks_var, 0, 3)
        row_counter += 1

        self.create_snack_quality_widget(form_container, row_counter, col, "Качество перекусов:",
                                         self.snack_quality_var)
        row_counter += 1

        self.create_spinbox_widget(form_container, row_counter, col,
                                   "Вода (мл):", self.water_var, 200, 3000, 250)
        row_counter += 1

        self.create_spinbox_widget(form_container, row_counter, col, "Кофе (200мл):", self.caffeine_var, 0, 5)
        row_counter += 1

        self.create_spinbox_widget(form_container, row_counter, col, "Алкоголь (порция):", self.alcohol_var, 0, 5)
        row_counter += 1

        self.create_regularity_widget(form_container, row_counter, col, "Количество приемов пищи:", self.regularity_var)
        row_counter += 1

        options_label = tk.Label(
            form_container,
            text="Дополнительные параметры:",
            font=('Arial', 14, 'bold'),
            bg='lightblue',
            fg='black'
        )
        options_label.grid(row=row_counter, column=2, columnspan=5, pady=10, sticky='ew')
        row_counter += 1

        options_frame = tk.Frame(form_container, bg='lightblue')
        options_frame.grid(row=row_counter, column=0, columnspan=9, pady=5, sticky='ew')

        for i in range(9):
            options_frame.grid_columnconfigure(i, weight=1)

        fermented_cb = tk.Checkbutton(options_frame, text="Ферментированные продукты \n (квашеные овощи, йогурты)",
                                      variable=self.fermented_var, bg='lightblue', fg='black',
                                      font=('Arial', 12, 'bold'))
        fermented_cb.grid(row=0, column=3, padx=10, sticky='w')

        green_tea_cb = tk.Checkbutton(options_frame, text="Зеленый чай",
                                      variable=self.green_tea_var, bg='lightblue', fg='black',
                                      font=('Arial', 12, 'bold'))
        green_tea_cb.grid(row=0, column=5, padx=10, sticky='w')

        magnesium_cb = tk.Checkbutton(options_frame, text="Продукты с магнием \n(шпинат, брокколи, бананы, орехи) ",
                                      variable=self.magnesium_var, bg='lightblue', fg='black',
                                      font=('Arial', 12, 'bold'))
        magnesium_cb.grid(row=0, column=7, padx=10, sticky='w')

        if self.is_premium:
            nav_frame = tk.Frame(self.frame, bg='lightblue')
            nav_frame.grid(row=4, column=0, columnspan=5, pady=10, sticky='ew')

            for i in range(6):
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
            self.next_button.grid(row=0, column=5, padx=5, sticky='w')

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
        back_button.grid(row=8, column=0, columnspan=5, pady=5, sticky='s')

        self.update_day_display()
        self.update_navigation_buttons()

    def create_spinbox_widget(self, parent, row, col, label_text, variable, from_, to, increment=1):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        label = tk.Label(container, text=label_text, font=('Arial', 14, 'bold'), bg='lightblue', fg='black')
        label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        spinbox = tk.Spinbox(
            container,
            from_=from_,
            to=to,
            increment=increment,
            textvariable=variable,
            width=10,
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='black',
            state='readonly'
        )
        spinbox.grid(row=0, column=1, sticky='w', padx=5)
        return spinbox

    def create_quality_widget(self, parent, row, col, label_text, variable):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        label = tk.Label(container, text=label_text, font=('Arial', 14, 'bold'), bg='lightblue', fg='black')
        label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        quality_frame = tk.Frame(container, bg='lightblue')
        quality_frame.grid(row=0, column=1, columnspan=2, sticky='w')

        options = [
            ("Низкое", 0),
            ("Среднее", 1),
            ("Высокое", 2)
        ]

        for i, (text, value) in enumerate(options):
            rb = tk.Radiobutton(quality_frame, text=text, variable=variable, value=value,
                                bg='lightblue', fg='black', font=('Arial', 12, 'bold'))
            rb.grid(row=0, column=i, padx=8)
        return quality_frame

    def create_snack_quality_widget(self, parent, row, col, label_text, variable):
        return self.create_quality_widget(parent, row, col, label_text, variable)

    def create_regularity_widget(self, parent, row, col, label_text, variable):
        container = tk.Frame(parent, bg='lightblue')
        container.grid(row=row, column=col, columnspan=3, pady=8, sticky='ew')

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

        label = tk.Label(container, text=label_text, font=('Arial', 14, 'bold'), bg='lightblue', fg='black')
        label.grid(row=0, column=0, sticky='e', padx=(0, 10))

        regularity_frame = tk.Frame(container, bg='lightblue')
        regularity_frame.grid(row=0, column=1, columnspan=2, sticky='w')

        options = [
            ("1-2", 0),
            ("3-4", 1),
            ("5-6", 2)
        ]

        for i, (text, value) in enumerate(options):
            rb = tk.Radiobutton(regularity_frame, text=text, variable=variable, value=value,
                                bg='lightblue', fg='black', font=('Arial', 12, 'bold'))
            rb.grid(row=0, column=i, padx=8)
        return regularity_frame

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
            'quality': self.quality_var.get(),
            'snacks': self.snacks_var.get(),
            'snack_quality': self.snack_quality_var.get(),
            'water': self.water_var.get(),
            'caffeine': self.caffeine_var.get(),
            'alcohol': self.alcohol_var.get(),
            'regularity': self.regularity_var.get(),
            'fermented': self.fermented_var.get(),
            'green_tea': self.green_tea_var.get(),
            'magnesium': self.magnesium_var.get()
        }

        while len(self.food_data) < self.current_day:
            self.food_data.append({
                'quality': 1, 'snacks': 1, 'snack_quality': 1, 'water': 1.0,
                'caffeine': 1, 'alcohol': 0, 'regularity': 1,
                'fermented': False, 'green_tea': False, 'magnesium': False
            })

        self.food_data[self.current_day - 1] = day_data

    def update_day_display(self):
        self.day_label.config(text=f"День {self.current_day}")

        if len(self.food_data) >= self.current_day:
            day_data = self.food_data[self.current_day - 1]
            self.quality_var.set(day_data['quality'])
            self.snacks_var.set(day_data['snacks'])
            self.snack_quality_var.set(day_data['snack_quality'])
            self.water_var.set(day_data['water'])
            self.caffeine_var.set(day_data['caffeine'])
            self.alcohol_var.set(day_data['alcohol'])
            self.regularity_var.set(day_data['regularity'])
            self.fermented_var.set(day_data['fermented'])
            self.green_tea_var.set(day_data['green_tea'])
            self.magnesium_var.set(day_data['magnesium'])

    def update_navigation_buttons(self):
        if self.is_premium:
            self.prev_button.config(state='normal' if self.current_day > 1 else 'disabled')
            self.next_button.config(state='normal')



    def go_back(self):
        self.app.show_main_menu()