from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager
from database import init_db
from location_check import LocationCheckScreen
from scanner import ScannerScreen

# डेटाबेस इनिशियलाइज़ करें
init_db()

class LoginScreen(MDScreen):
    def check_login(self): 
        username = self.ids.username.text
        password = self.ids.password.text

        if username == "admin" and password == "1234":
            self.manager.current = "location"
        else:
            self.show_dialog("Login Failed", "Invalid username or password")

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(
                text="OK",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                on_release=lambda x: dialog.dismiss()
            )],
        )
        dialog.open()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"  # Light theme for better visibility
        Window.size = (300, 600)
        return Builder.load_file('home.kv')
    
    def on_start(self):
        self.school_location = (19.0760, 72.8777)

if __name__ == "__main__":
    MainApp().run()
