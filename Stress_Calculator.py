import tkinter as tk
from ContextMenu import ContextMenu
from MatrixLicenseGenerator import MatrixLicenseGenerator
from Sleep_Frame import SleepFrame
from Food_Frame import FoodFrame
from Activity_Frame import ActivityFrame
from Emotion_Frame import EmotionFrame
from Activation import ActivationFrame
from Main import MainMenuFrame
from Result import ResultFrame
from Welcome import WelcomeScreenFrame

class StressCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Контроль стресса")
        self.root.geometry("2560x1600")
        self.root.configure(bg='lightblue')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.license_generator = MatrixLicenseGenerator()
        self.context_menu = ContextMenu(root)
        self.is_premium = False

        self.setup_main_screen()

    def setup_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.welcome_screen_frame = WelcomeScreenFrame(self.root, self)
        self.welcome_screen_frame.frame.grid(row=0, column=0, sticky="nsew")

    def free_version_click(self):
        self.is_premium = False
        self.show_main_menu()

    def premium_version_click(self):
        self.show_activation_window()

    def show_activation_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.activation_frame = ActivationFrame(self.root, self)
        self.activation_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_menu_frame = MainMenuFrame(self.root, self)
        self.main_menu_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_sleep_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.sleep_frame = SleepFrame(self.root, self, self.is_premium)
        self.sleep_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_food_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.food_frame = FoodFrame(self.root, self, self.is_premium)
        self.food_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_activity_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.activity_frame = ActivityFrame(self.root, self, self.is_premium)
        self.activity_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_emotion_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.emotion_frame = EmotionFrame(self.root, self, self.is_premium)
        self.emotion_frame.frame.grid(row=0, column=0, sticky="nsew")

    def show_result_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.result_frame = ResultFrame(self.root, self)
        self.result_frame.frame.grid(row=0, column=0, sticky="nsew")

root = tk.Tk()
app = StressCalculatorApp(root)
root.mainloop()