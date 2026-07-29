import numpy as np
import tkinter as tk
from matplotlib import gridspec, pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Activity_Model import ActivityModel
from Emotional_Model import EmotionModel
from Food_Model import FoodModel
from Integrated import IntegratedStressSystem
from SleepModel import SleepModel
from Recommend import Recommendation


class OverallResultFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='white')
        self.app = app
        self.current_view = "graphs"
        self.results = None
        self.recommend = Recommendation()
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(12):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.frame.grid_columnconfigure(i, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Общий анализ уровня стресса",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=5)

        button_frame = tk.Frame(self.frame, bg='white')
        button_frame.grid(row=1, column=0, columnspan=3, pady=2)

        self.show_graphs_button = tk.Button(
            button_frame,
            text="Показать графики",
            font=('Arial', 12, 'bold'),
            bg='blue',
            fg='white',
            width=20,
            height=1,
            command=self.show_graphs_view
        )
        self.show_graphs_button.pack(side=tk.LEFT, padx=5)

        self.show_recommendations_button = tk.Button(
            button_frame,
            text="Показать рекомендации",
            font=('Arial', 12, 'bold'),
            bg='green',
            fg='white',
            width=20,
            height=1,
            command=self.show_recommendations_view
        )
        self.show_recommendations_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(
            button_frame,
            text="Назад к результатам",
            font=('Arial', 12),
            bg='grey',
            fg='white',
            width=20,
            height=1,
            command=self.go_back
        )
        back_button.pack(side=tk.LEFT, padx=5)

        self.content_frame = tk.Frame(self.frame, bg='white')
        self.content_frame.grid(row=2, column=0, columnspan=3, rowspan=10,
                                sticky='nsew', padx=10, pady=5)

        try:
            self.results = self.analyze_overall_data()
            self.show_graphs_view()
        except Exception as e:
            error_label = tk.Label(
                self.content_frame,
                text=f"Ошибка загрузки данных: {str(e)}",
                font=('Arial', 14),
                bg='white',
                fg='red'
            )
            error_label.pack(expand=True)

    def show_graphs_view(self):
        self.current_view = "graphs"
        self.update_button_states()
        self.clear_content_frame()
        if self.results:
            self.create_graphs(self.results)

    def show_recommendations_view(self):
        self.current_view = "recommendations"
        self.update_button_states()
        self.clear_content_frame()
        if self.results:
            self.create_recommendations(self.results)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_button_states(self):
        if self.current_view == "graphs":
            self.show_graphs_button.config(bg='darkblue', state='disabled')
            self.show_recommendations_button.config(bg='green', state='normal')
        else:
            self.show_graphs_button.config(bg='blue', state='normal')
            self.show_recommendations_button.config(bg='darkgreen', state='disabled')

    def create_graphs(self, results):
        fig = Figure(figsize=(13, 8), dpi=100)
        fig.patch.set_facecolor('white')
        gs = gridspec.GridSpec(3, 1, figure=fig, hspace=0.4)

        ax1 = fig.add_subplot(gs[0, 0])
        self.create_stress_timeline(ax1, results)

        ax2 = fig.add_subplot(gs[1, 0])
        self.create_efficiency_summary(ax2, results)

        ax3 = fig.add_subplot(gs[2, 0])
        self.create_progress_tracker(ax3, results)

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_stress_timeline(self, ax, results):
        if 'daily_stress' in results and results['daily_stress']:
            days = list(range(1, len(results['daily_stress']) + 1))
            stress_levels = results['daily_stress']

            ax.fill_between(days, stress_levels, alpha=0.2, color='#d62728')
            ax.axhline(y=8, color='red', linestyle='--', alpha=0.7, label='Критический (8+)')
            ax.axhline(y=6, color='orange', linestyle='--', alpha=0.7, label='Высокий (6-8)')
            ax.axhline(y=4, color='green', linestyle='--', alpha=0.7, label='Нормальный (4-6)')

            for day, stress in zip(days, stress_levels):
                ax.text(day, stress + 0.2, f'{stress:.1f}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

            ax.set_xticks(days)
            ax.set_xticklabels([f'День {d}' for d in days])
        else:
            current_stress = results['total_stress']
            ax.bar(['Текущий уровень'], [current_stress],
                   color='#d62728', alpha=0.7, label='Общий стресс')
            ax.text(0, current_stress + 0.2, f'{current_stress:.1f}/10',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_xlabel('Дни')
        ax.set_ylabel('Уровень стресса (1-10)')
        ax.set_title('Динамика общего стресса', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 10.5)
        ax.set_yticks(range(0, 11))
        ax.grid(True, alpha=0.3)
        ax.legend()

    def create_efficiency_summary(self, ax, results):
        categories = ['Сон', 'Питание', 'Активность', 'Эмоции']
        scores = [
            results['sleep_score'],
            results['food_score'],
            results['activity_score'],
            results['emotion_score']
        ]

        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']
        ax.axis('off')

        total_score = results['total_stress']
        status_color = '#2ca02c' if total_score <= 5 else '#ff7f0e' if total_score <= 7 else '#d62728'

        ax.text(0.5, 0.9, f"Общий стресс: {total_score:.1f}/10",
                fontsize=14, fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=status_color, linewidth=2))

        for i, (category, score, color) in enumerate(zip(categories, scores, colors)):
            x_pos = 0.2 + i * 0.2
            y_pos = 0.55

            circle = plt.Circle((x_pos, y_pos), 0.08, color=color, alpha=0.7)
            ax.add_patch(circle)
            ax.text(x_pos, y_pos, f'{score:.1f}',
                    ha='center', va='center', fontweight='bold', color='white', fontsize=10)

            ax.text(x_pos, 0.38, category, ha='center', va='center', fontsize=10)

            status = "✓" if score <= 5 else "~" if score <= 7 else "!"
            ax.text(x_pos, 0.70, status,
                    ha='center', va='center', fontsize=14, fontweight='bold',
                    color='green' if score <= 5 else 'orange' if score <= 7 else 'red',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))

        worst_category = categories[scores.index(max(scores))]
        ax.text(0.5, 0.15, f"Самая проблемная: {worst_category}",
                fontsize=11, ha='center', va='center', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='#ff7f0e', alpha=0.3))

    def create_progress_tracker(self, ax, results):
        categories = ['Сон', 'Питание', 'Активность', 'Эмоции']
        scores = [
            results['sleep_score'],
            results['food_score'],
            results['activity_score'],
            results['emotion_score']
        ]

        progress = [max(0, 10 - score) for score in scores]
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']
        y_pos = np.arange(len(categories))

        bars = ax.barh(y_pos, progress, color=colors, alpha=0.7, label='Баланс')
        ax.axvline(x=10, color='black', linestyle='--', alpha=0.5, label='Идеал')

        for bar, score, prog in zip(bars, scores, progress):
            width = bar.get_width()
            ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2,
                    f'{score:.1f}/10', va='center', fontweight='bold')

            status = "✓" if score <= 5 else "➡" if score <= 7 else "⚠"
            ax.text(-0.8, bar.get_y() + bar.get_height() / 2, status,
                    va='center', fontweight='bold', fontsize=12,
                    color='green' if score <= 5 else 'orange' if score <= 7 else 'red',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7))

        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories)
        ax.set_xlabel('Уровень баланса (10 = идеал)')
        ax.set_title('Прогресс по категориям', fontsize=14, fontweight='bold')
        ax.set_xlim(-1, 11)
        ax.grid(True, alpha=0.3, axis='x')
        ax.legend()

        total_progress = sum(progress) / len(progress)
        ax.text(0.02, 0.98, f"Общий баланс: {total_progress:.1f}/10",
                transform=ax.transAxes, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white'))

    def create_recommendations(self, results):
        main_frame = tk.Frame(self.content_frame, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        title_label = tk.Label(
            main_frame,
            text="Общие рекомендации",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='black'
        )
        title_label.pack(pady=3)

        score_label = tk.Label(
            main_frame,
            text=f"Общий уровень стресса: {results['total_stress']}/10",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='blue'
        )
        score_label.pack(pady=2)

        text_widget = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=('Arial', 12),
            bg='white',
            fg='black',
            padx=10,
            pady=10,
            width=80,
            height=15,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        text_widget.pack(pady=10, padx=10)

        for i, recommendation in enumerate(results['recommendations'], 1):
            text_widget.insert(tk.END, f" {recommendation}\n\n")

        text_widget.config(state=tk.DISABLED)

    def analyze_overall_data(self):
        try:
            sleep_data = self.get_valid_data('sleep')
            food_data = self.get_valid_data('food')
            activity_data = self.get_valid_data('activity')
            emotion_data = self.get_valid_data('emotion')

            if not all([sleep_data, food_data, activity_data, emotion_data]):
                error_msg = f"Не все данные заполнены. Заполните все разделы для полного анализа.\n"
                error_msg += f"Сон: {'✓' if sleep_data else '✗'}, Питание: {'✓' if food_data else '✗'}, "
                error_msg += f"Активность: {'✓' if activity_data else '✗'}, Эмоции: {'✓' if emotion_data else '✗'}"
                raise Exception(error_msg)

            sleep_model = SleepModel()
            food_model = FoodModel()
            activity_model = ActivityModel()
            emotion_model = EmotionModel()

            sleep_result = sleep_model.periodic_stress(sleep_data)
            sleep_score = sleep_result['stress_score'] if isinstance(sleep_result, dict) else sleep_result
            food_score = food_model.periodic_stress(food_data)
            activity_score = activity_model.periodic_stress(activity_data)
            emotion_score = emotion_model.periodic_stress(emotion_data)

            sleep_score = max(0, min(float(sleep_score), 10))
            food_score = max(0, min(float(food_score), 10))
            activity_score = max(0, min(float(activity_score), 10))
            emotion_score = max(0, min(float(emotion_score), 10))

            integrated_model = IntegratedStressSystem()
            total_stress = integrated_model.calculate_stress(
                sleep_score, food_score, activity_score, emotion_score
            )

            daily_stress_scores = self.calculate_daily_stress(
                sleep_data, food_data, activity_data, emotion_data,
                sleep_score, food_score, activity_score, emotion_score,
                sleep_model, food_model, activity_model, emotion_model
            )

            recommendations = self.generate_overall_recommendations(
                sleep_score, food_score, activity_score, emotion_score, total_stress
            )

            return {
                'total_stress': round(total_stress, 1),
                'sleep_score': round(sleep_score, 1),
                'food_score': round(food_score, 1),
                'activity_score': round(activity_score, 1),
                'emotion_score': round(emotion_score, 1),
                'daily_stress': daily_stress_scores,
                'recommendations': recommendations
            }

        except Exception as e:
            raise Exception(f"Ошибка анализа данных: {str(e)}")

    def calculate_daily_stress(self, sleep_data, food_data, activity_data, emotion_data,
                               sleep_score, food_score, activity_score, emotion_score,
                               sleep_model, food_model, activity_model, emotion_model):
        daily_stress_scores = []
        min_days = min(len(sleep_data), len(food_data), len(activity_data), len(emotion_data))

        for i in range(min_days):
            daily_scores = []

            if i < len(sleep_data):
                try:
                    bed_time, wake_time = sleep_data[i]
                    duration, deficit, mid, circ_align = sleep_model.daily_metrics(bed_time, wake_time)
                    daily_sleep_score = min(10, max(0, deficit * 1.5 + circ_align * 0.3))
                    daily_scores.append(daily_sleep_score)
                except Exception:
                    daily_scores.append(sleep_score)

            if i < len(food_data):
                try:
                    daily_food_score = food_model.daily_stress(food_data[i]) * 10
                    daily_food_score = max(0, min(daily_food_score, 10))
                    daily_scores.append(daily_food_score)
                except Exception:
                    daily_scores.append(food_score)

            if i < len(activity_data):
                try:
                    daily_activity_score = activity_model.daily_stress(activity_data[i]) * 10
                    daily_activity_score = max(0, min(daily_activity_score, 10))
                    daily_scores.append(daily_activity_score)
                except Exception:
                    daily_scores.append(activity_score)

            if i < len(emotion_data):
                try:
                    daily_emotion_score = emotion_model.daily_stress(emotion_data[i]) * 10
                    daily_emotion_score = max(0, min(daily_emotion_score, 10))
                    daily_scores.append(daily_emotion_score)
                except Exception:
                    daily_scores.append(emotion_score)

            if daily_scores:
                daily_score = sum(daily_scores) / len(daily_scores)
                daily_stress_scores.append(min(10, daily_score))

        return daily_stress_scores

    def get_valid_data(self, category):
        frame_attr_map = {
            'sleep': ('sleep_frame', 'sleep_schedule', lambda day: day[0] and day[1]),
            'food': ('food_frame', 'food_data', lambda day: day is not None),
            'activity': ('activity_frame', 'activity_data', lambda day: day is not None),
            'emotion': ('emotion_frame', 'emotion_data', lambda day: day is not None)
        }

        if category not in frame_attr_map:
            return None

        frame_attr, data_attr, validator = frame_attr_map[category]

        if not hasattr(self.app, frame_attr):
            return None

        frame = getattr(self.app, frame_attr)
        data = getattr(frame, data_attr, [])

        if not data:
            return None

        valid_days = [day for day in data if validator(day)]
        return valid_days if valid_days else None

    def generate_overall_recommendations(self, sleep_score, food_score, activity_score,
                                         emotion_score, total_stress):
        recommendations = []
        rec = self.recommend.get_all_recommendations()

        if not rec:
            return recommendations

        if total_stress >= 8:
            recommendations.append(rec['critical_level'])
        elif total_stress >= 6:
            recommendations.append(rec['high_level'])
        elif total_stress >= 4:
            recommendations.append(rec['medium_level'])
        else:
            recommendations.append(rec['good_level'])

        if sleep_score >= 6 and emotion_score >= 6:
            recommendations.append(rec['sleep_emotion_interaction'])

        if activity_score >= 6 and sleep_score >= 6:
            recommendations.append(rec['activity_sleep_interaction'])

        if food_score >= 6 and activity_score >= 6:
            recommendations.append(rec['food_activity_interaction'])

        if food_score >= 6 and emotion_score >= 6:
            recommendations.append(rec['food_emotion_interaction'])

        scores_dict = {
            'Сон': sleep_score,
            'Питание': food_score,
            'Активность': activity_score,
            'Эмоции': emotion_score
        }
        worst_factor = max(scores_dict.items(), key=lambda x: x[1])

        if worst_factor[1] >= 6:
            recommendations.append(
                rec['improvement_strategy'].format(
                    category=worst_factor[0],
                    score=worst_factor[1]
                )
            )

        return recommendations

    def go_back(self):
        self.app.show_result_frame()