import json
import os


class Recommendation:
    def __init__(self, json_path='recommendations.json'):
        self.json_path = json_path
        self.recommendations = {}
        self.load_recommendations()

    def load_recommendations(self):
        try:
            if not os.path.exists(self.json_path):
                raise FileNotFoundError(f"Файл {self.json_path} не найден")

            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.recommendations = json.load(f)

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            print("Создайте файл с рекомендациями или укажите правильный путь.")
            self.recommendations = {}
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON файла: {e}")
            self.recommendations = {}
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            self.recommendations = {}

    def get_recommendation(self, key, default=None):
        return self.recommendations.get(key, default)

    def get_all_recommendations(self):
        return self.recommendations.copy()