from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
from database import mark_attendance
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

SCHOOL_QR_CODE = "SCHOOL_12345"

class ScannerScreen(MDScreen):
    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.img = Image()
        self.ids.camera_view.add_widget(self.img)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # QR कोड डिटेक्ट करें
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(frame)
            
            if data:
                # QR कोड वैलिडेट करें
                if data == SCHOOL_QR_CODE:
                    mark_attendance("STU001", "Present")
                    self.show_result("उपस्थिति दर्ज", "आपकी उपस्थिति दर्ज की गई!")
                else:
                    self.show_result("गलत QR कोड", "यह स्कूल का QR कोड नहीं है")
            
            # कैमरा दिखाएँ
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def show_result(self, title, text):
        self.capture.release()
        Clock.unschedule(self.update)
        
        # डायलॉग बंद करने और लॉगिन स्क्रीन पर जाने का फंक्शन
        def close_dialog_and_go_login(instance):
            dialog.dismiss()
            self.manager.current = "login"
        
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=close_dialog_and_go_login
                )
            ],
        )
        dialog.open()

    def on_leave(self):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
        Clock.unschedule(self.update)
