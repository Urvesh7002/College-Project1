from plyer import gps
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.app import App
from database import mark_attendance

class LocationCheckScreen(MDScreen):
    def on_enter(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=0)
        except NotImplementedError:
            self.show_dialog("GPS त्रुटि", "इस डिवाइस में GPS सपोर्ट नहीं है")

    def on_location(self, **kwargs):
        app = App.get_running_app()
        try:
            lat = kwargs['lat']
            lon = kwargs['lon']
            college_lat, college_lon = app.school_location  # ✅ नाम बदल सकते हो app.college_location भी कर सकते हो
            
            # दूरी चेक करें
            distance = ((lat - college_lat)**2 + (lon - college_lon)**2)**0.5
            
            if distance < 0.01:  # ~1km के अंदर
                self.manager.current = "scanner"
            else:
                self.show_dialog("गलत स्थान", "आप कॉलेज में नहीं हैं!")  # ✅ बदला गया
                mark_attendance("STU001", "Absent")
        except KeyError:
            pass

    def show_dialog(self, title, message):
        def close_dialog_and_go_login(instance):
            dialog.dismiss()
            self.manager.current = "login"
        
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=close_dialog_and_go_login
                )
            ]
        )
        dialog.open()

    def on_leave(self):
        gps.stop()
