# scanner.py

from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2

class ScannerScreen(MDScreen):
    def on_enter(self):
        # कैमरा चालू करो
        self.capture = cv2.VideoCapture(0)
        self.img = Image()
        self.add_widget(self.img)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # QR Code डिटेक्ट करने का काम
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(frame)

            # अगर कुछ स्कैन हुआ है
            if data:
                print("QR Code Data:", data)
                self.capture.release()
                Clock.unschedule(self.update)
                self.show_result(data)
                return

            # स्क्रीन पर कैमरा दिखाओ
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def show_result(self, data):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton

        dialog = MDDialog(
            title="QR Code Scanned ✅",
            text=f"Student ID: {data}",
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())
            ],
        )
        dialog.open()
