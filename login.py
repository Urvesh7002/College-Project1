from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from pymongo import MongoClient

class LoginApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Connect to MongoDB Atlas (replace <connection_string> with your actual connection string)
        self.client = MongoClient("<connection_string>")
        self.db = self.client["college_project"]  # Database name
        self.collection = self.db["users"]       # Collection name

    def build(self):
        # Create the main screen
        screen = MDScreen()

        # Username field
        self.username = MDTextField(
            hint_text="Username",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint_x=0.8
        )
        screen.add_widget(self.username)

        # Password field
        self.password = MDTextField(
            hint_text="Password",
            password=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint_x=0.8
        )
        screen.add_widget(self.password)

        # Login button
        login_button = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.validate_credentials
        )
        screen.add_widget(login_button)

        # Error label (hidden by default)
        self.error_label = MDLabel(
            text="",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            theme_text_color="Error"
        )
        screen.add_widget(self.error_label)

        return screen

    def validate_credentials(self, instance):
        username = self.username.text
        password = self.password.text

        # Query MongoDB for the user
        user = self.collection.find_one({"username": username, "password": password})

        if user:
            self.show_dialog("Login Successful", f"Welcome, {username}!")
        else:
            self.error_label.text = "Invalid username or password"

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

if __name__ == "__main__":
    LoginApp().run()
