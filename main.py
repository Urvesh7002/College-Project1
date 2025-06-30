from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from database import init_db, add_user, check_user_credentials, username_exists
from location_check import LocationCheckScreen
from scanner import ScannerScreen

init_db()

class LoginScreen(MDScreen):
    def check_login(self): 
        username = self.ids.username.text
        password = self.ids.password.text

        if not username_exists(username):
            self.ids.error_label.text = "Username is incorrect"
        elif not check_user_credentials(username, password):
            self.ids.error_label.text = "Password is incorrect"
        else:
            self.ids.error_label.text = ""
            app = MDApp.get_running_app()
            app.current_user = username  # Set current user
            self.manager.current = "location"

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
            self.manager.current = "location"

        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=go_to_location)]
        )
        dialog.open()

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Window.size = (300, 600)
        self.current_user = None  # To store logged-in user
        return Builder.load_file('home.kv')

    def on_start(self):
        self.college_location = (19.0760, 72.8777)  # College location coordinates

if __name__ == "__main__":
    MainApp().run()