from plyer import gps
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

class LocationCheckScreen(MDScreen):
    def on_enter(self):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(minTime=1000, minDistance=1)
        except NotImplementedError:
            self.show_dialog("❌ GPS Error", "GPS इस डिवाइस में काम नहीं कर रहा।")

    def on_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')

        print(f"📍 Current Location: {lat}, {lon}")

        # Admin Set Location
        school_lat = 19.0760
        school_lon = 72.8777

        # Distance Check
        distance = abs(float(lat) - school_lat) + abs(float(lon) - school_lon)

        if distance < 0.01:
            self.show_dialog("✅ Location OK", "आप स्कूल में हो, QR स्कैन करो।")
        else:
            self.show_dialog("❌ Location Blocked", "आप स्कूल में नहीं हो।")

    def on_status(self, stype, status):
        print(f"🔄 GPS status: {stype} = {status}")

    def show_dialog(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()
