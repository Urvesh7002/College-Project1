from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

class LoginScreen(MDScreen):
    def check_login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if username == "admin" and password == "1234":
            self.show_dialog("Login Successful!", "Welcome!")
        else:
            self.show_dialog("Login Failed", "Invalid username or password")

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return LoginScreen()

LoginApp().run()
