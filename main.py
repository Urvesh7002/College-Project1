from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from database import init_db, add_user, check_user_credentials
from location_check import LocationCheckScreen
from scanner import ScannerScreen

init_db()

class LoginScreen(MDScreen):
    def check_login(self): 
        username = self.ids.username.text
        password = self.ids.password.text

        if check_user_credentials(username, password):
            self.manager.current = "location"
        else:
            self.show_dialog("Login Failed", "Invalid username or password")

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

class SignUpScreen(MDScreen):
    def signup_user(self):
        username = self.ids.signup_username.text
        password = self.ids.signup_password.text
        name = self.ids.signup_name.text

        if username == "" or password == "" or name == "":
            self.show_dialog("Error", "Please fill all fields")
            return

        success = add_user(username, password, name)
        if success:
            self.show_dialog_and_go("Success", "Account created! Redirecting...")
        else:
            self.show_dialog("Error", "Username already exists")

    def show_dialog_and_go(self, title, text):
        def go_to_location(instance):
            dialog.dismiss()
            self.manager.current = "location"  # ✅ सीधे location checker पर जाए

        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=go_to_location)
            ]
        )
        dialog.open()

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Window.size = (300, 600)
        return Builder.load_file('home.kv')

    def on_start(self):
        self.school_location = (19.0760, 72.8777)  # मुंबई के latitude/longitude

if __name__ == "__main__":
    MainApp().run()
