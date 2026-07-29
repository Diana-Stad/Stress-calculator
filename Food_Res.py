import tkinter as tk
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Food_Model import FoodModel


class FoodResultFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='white')
        self.app = app
        self.results = None
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(8):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.frame.grid_columnconfigure(i, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Результаты анализа питания",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=3)

        button_frame = tk.Frame(self.frame, bg='white')
        button_frame.grid(row=1, column=0, columnspan=3, pady=2)

        back_button = tk.Button(
            button_frame,
            text="Назад к результатам",
            font=('Arial', 12),
            bg='grey',
            fg='white',
            width=18,
            height=1,
            command=self.go_back
        )
        back_button.pack(side=tk.LEFT, padx=5)

        self.content_frame = tk.Frame(self.frame, bg='white')
        self.content_frame.grid(row=2, column=0, columnspan=3, rowspan=6,
                                sticky='nsew', padx=10, pady=3)

        try:
            self.results = self.analyze_food_data()
            self.show_graphs_view()
        except Exception as e:
            error_label = tk.Label(
                self.content_frame,
                text=f"Ошибка загрузки данных: {str(e)}",
                font=('Arial', 12),
                bg='white',
                fg='red'
            )
            error_label.pack(expand=True)

    def show_graphs_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_graphs(self.results)

    def create_graphs(self, results):
        fig = Figure(figsize=(12, 8), dpi=100)
        fig.patch.set_facecolor('white')

        gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

        ax1 = fig.add_subplot(gs[0, 0])
        self.create_food_balance_chart(ax1, results['food_data'], results['food_model'])

        ax2 = fig.add_subplot(gs[0, 1])
        self.create_food_impact_analysis(ax2, results['food_data'])

        ax3 = fig.add_subplot(gs[1, :])
        self.create_daily_food_patterns(ax3, results['food_data'], results['food_model'])

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_food_balance_chart(self, ax, food_data, food_model):
        good_days = 0
        neutral_days = 0
        bad_days = 0

        for day in food_data:
            daily_score = food_model.daily_stress(day) * 10
            if daily_score >= 7:
                good_days += 1
            elif daily_score >= 4:
                neutral_days += 1
            else:
                bad_days += 1

        total_days = len(food_data)

        sizes = [good_days, neutral_days, bad_days]
        labels = [f'Полезное\n{good_days} дн.',
                  f'Нейтральное\n{neutral_days} дн.',
                  f'Вредное\n{bad_days} дн.']
        colors = ['#2ca02c', '#ff7f0e', '#d62728']

        wedges, texts = ax.pie(sizes, colors=colors, startangle=90)

        ax.legend(wedges, labels, title="Типы питания",
                  loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))

        center_text = f"Всего:\n{total_days} дн."
        ax.text(0, 0, center_text, ha='center', va='center',
                fontsize=10, fontweight='bold')

        ax.set_title('Баланс питания', fontsize=12, fontweight='bold', pad=15)

    def create_food_impact_analysis(self, ax, food_data):
        problem_days = {}

        for day in food_data:
            if day['caffeine'] > 2:
                problem_days['Высокий кофеин'] = problem_days.get('Высокий кофеин', 0) + 1
            if day['water'] < 1:
                problem_days['Мало воды'] = problem_days.get('Мало воды', 0) + 1
            if day['snack_quality'] == 0 and day['snacks'] > 0:
                problem_days['Вредные перекусы'] = problem_days.get('Вредные перекусы', 0) + 1
            if day['alcohol'] > 0:
                problem_days['Алкоголь'] = problem_days.get('Алкоголь', 0) + 1
            if day['regularity'] == 0:
                problem_days['Нерегулярность'] = problem_days.get('Нерегулярность', 0) + 1
            if day['quality'] == 0:
                problem_days['Низкое качество'] = problem_days.get('Низкое качество', 0) + 1

        if not problem_days:
            ax.text(0.5, 0.5, "Проблем не\nобнаружено!",
                    ha='center', va='center', fontsize=12, fontweight='bold')
            ax.set_title('Анализ проблем', fontsize=12, fontweight='bold')
            return

        sorted_items = sorted(problem_days.items(), key=lambda x: x[1], reverse=True)
        problem_names, problem_counts = zip(*sorted_items)

        y_pos = list(range(len(problem_names)))
        colors = ['#d62728', '#ff7f0e', '#ff7f0e', '#1f77b4', '#1f77b4', '#1f77b4']

        bars = ax.barh(y_pos, problem_counts, color=colors[:len(problem_names)], alpha=0.7)

        for bar, count in zip(bars, problem_counts):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                    f'{count} дн.', va='center', fontweight='bold', fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(problem_names, fontsize=9)
        ax.set_xlabel('Дней с проблемой')
        ax.set_title('Частые проблемы питания', fontsize=12, fontweight='bold')

        max_count = max(problem_counts)
        ax.set_xlim(0, max_count + 1)
        ax.set_xticks(range(0, max_count + 2))
        ax.grid(True, alpha=0.3, axis='x')

    def create_daily_food_patterns(self, ax, food_data, food_model):
        days = list(range(1, len(food_data) + 1))
        cumulative_scores = []

        for i in range(1, len(food_data) + 1):
            period_data = food_data[:i]
            score = food_model.periodic_stress(period_data)
            cumulative_scores.append(score)

        ax.fill_between(days, cumulative_scores, alpha=0.2, color='#2ca02c')

        ax.axhline(y=3, color='green', linestyle='--', alpha=0.7, label='Отлично (<3)')
        ax.axhline(y=5, color='orange', linestyle='--', alpha=0.7, label='Нормально (3-5)')
        ax.axhline(y=7, color='red', linestyle='--', alpha=0.7, label='Плохо (>7)')

        for day, score in zip(days, cumulative_scores):
            ax.text(day, score + 0.3, f'{score:.1f}',
                    ha='center', va='bottom', fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

        ax.set_xlabel('Дни')
        ax.set_ylabel('Оценка питания')
        ax.set_title('Динамика оценки питания', fontsize=12, fontweight='bold')
        ax.set_xticks(days)
        ax.set_xticklabels([f'Д {d}' for d in days], fontsize=8)
        ax.set_ylim(0, 10.5)
        ax.set_yticks(range(0, 11))
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=8)

        ax.axhspan(0, 3, alpha=0.1, color='green')
        ax.axhspan(3, 7, alpha=0.1, color='orange')
        ax.axhspan(7, 10, alpha=0.1, color='red')

        final_score = cumulative_scores[-1] if cumulative_scores else 0
        status = "Отлично" if final_score < 3 else "Нормально" if final_score <= 7 else "Требует улучшений"

        stats_text = f"Итог: {final_score:.1f}/10\n{status}"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                fontsize=9, va='top', ha='left',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))


    def analyze_food_data(self):
        if hasattr(self.app, 'food_frame') and self.app.food_frame:
            food_data = self.app.food_frame.food_data
            valid_days = [day for day in food_data if any(day.values())]

            if not valid_days:
                raise Exception("Нет данных о питании для анализа.")

            food_model = FoodModel()
            food_score = food_model.periodic_stress(valid_days)

            return {
                'score': food_score,
                'food_data': valid_days,
                'food_model': food_model
            }
        else:
            raise Exception("Данные питания не заполнены.")

    def go_back(self):
        self.app.show_result_frame()