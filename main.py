from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from scanner import ScannerScreen
# Import your second screen
from location_check import LocationCheckScreen

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
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

# ✅ Move this class outside
class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("login.kv")

# ✅ Run the app
LoginApp().run()
