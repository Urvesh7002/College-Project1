import qrcode

# Create college QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("COLLEGE_12345")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("college_qr.png")
print("College QR code generated: college_qr.png")