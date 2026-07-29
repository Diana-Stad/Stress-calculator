import tkinter as tk


class ContextMenu:
    def __init__(self, root):
        self.root = root
        self.current_widget = None
        self.context_menu = None
        self.create_context_menu()

    def create_context_menu(self):
        if self.context_menu:
            try:
                self.context_menu.destroy()
            except:
                pass
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Вырезать", command=self.cut_text)
        self.context_menu.add_command(label="Копировать", command=self.copy_text)
        self.context_menu.add_command(label="Вставить", command=self.paste_text)

    def bind_to_widgets(self, widgets):
        for widget in widgets:
            widget.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.current_widget = event.widget
        self.update_menu_state()
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def update_menu_state(self):
        if self.current_widget is None:
            return
        try:
            try:
                if hasattr(self.current_widget, 'selection_get'):
                    selection = self.current_widget.selection_get()
                    has_selection = bool(selection.strip())
                else:
                    has_selection = False
            except:
                has_selection = False

            try:
                clipboard_text = self.root.clipboard_get()
                has_clipboard = bool(clipboard_text.strip())
            except:
                has_clipboard = False

            self.context_menu.entryconfig("Вырезать", state="normal" if has_selection else "disabled")
            self.context_menu.entryconfig("Копировать", state="normal" if has_selection else "disabled")
            self.context_menu.entryconfig("Вставить", state="normal" if has_clipboard else "disabled")

        except Exception:
            pass

    def cut_text(self):
        if self.current_widget:
            try:
                self.current_widget.event_generate('<<Cut>>')
            except:
                pass

    def copy_text(self):
        if self.current_widget:
            try:
                self.current_widget.event_generate('<<Copy>>')
            except:
                pass

    def paste_text(self):
        if self.current_widget:
            try:
                self.current_widget.event_generate('<<Paste>>')
            except:
                pass
